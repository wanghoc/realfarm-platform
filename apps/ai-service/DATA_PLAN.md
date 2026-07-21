# AI Service — Contract Schema Review & Image Data Plan

Companion notes to [ADR 0005](../../docs/adr/0005-ai-leaf-disease-mvp-candidate.md), covering the other two acceptance criteria of task #4: reviewing the existing contract schemas and planning the leaf-disease image data source.

## Contract schema review

Reviewed all four schemas in `packages/contracts/schemas`:

| Schema | Relevant to AI service? | Notes |
|---|---|---|
| `harvest-record.v1` | Indirect | Has `evidenceIds: string[]`, generic enough to later reference AI-detection evidence. No change needed now. |
| `iot-measurement.v1` | No | Sensor telemetry (temperature/humidity/soil/light/ph), not imagery. No overlap with disease detection. |
| `player-action-request.v1` | Indirect | A future "report suspected disease" player action could route through this generic request shape (`actionType` + free-form `parameters`). No change needed now — existing shape already supports it. |
| `work-order.v1` | Indirect | `items[].sourceRequestId` could point back to a player action or, later, an AI detection id, once one exists. No change needed now. |

**Finding:** none of the four existing schemas model an AI detection result. They don't need to change for this task, but a new schema is required before the AI baseline can be wired into the harvest/incident flow (targeted for Tuần 2 contract finalization, then real integration around Tuần 9-10 per the roadmap).

**Proposed new schema (for Tuần 2 discussion, not created yet):** `disease-detection-result.v1`

```text
detectionId       string (required)
imageRef          string (required)
plotId            string (required)
cropCycleId       string (required)
modelVersion      string (required)
predictedClass    string (required)
confidence        number, 0..1 (required)
status            enum: pending | needs_review | confirmed | dismissed (required)
detectedAt        string, date-time (required)
```

This mirrors the existing style (flat object, explicit enums, `additionalProperties: false`) and gives incident/work-order flows a stable id to reference, without the AI service writing to harvest or lease tables directly (keeps the non-goal in `apps/ai-service/README.md` intact).

## Image data source plan

- **Primary source (MVP baseline): PlantVillage**, a public leaf-image dataset with permissive terms for research/education use. Using a public dataset avoids the approval requirement in [12_SECURITY_AND_PRIVACY.md](../../docs/12_SECURITY_AND_PRIVACY.md#L24), which applies specifically to farm camera images.
- **Crop scope:** start with the Tomato subset of PlantVillage (healthy + disease classes), matching the crop the team is seeding into `crop_catalog` first (per [KE_HOACH_16_TUAN_CHI_TIET_VI.md:60](../../docs/KE_HOACH_16_TUAN_CHI_TIET_VI.md#L60)). Expand to additional crops only after the catalog grows.
- **Out of scope for now: real farm camera images.** They are not used for training until there is documented approval; camera setup with Khoa (Tuần 8, per the roadmap) is for *inference-time* snapshots, not automatic retraining data.
- **Local layout (not yet created, planned for the Tuần 8-9 data-collection step):**
  ```text
  apps/ai-service/data/
    raw/plantvillage/<class_name>/*.jpg      # downloaded subset, gitignored
    splits/train/<class_name>/...
    splits/val/<class_name>/...
    splits/test/<class_name>/...
  ```
  Raw datasets and any trained model binaries stay out of version control, per `CONTRIBUTING.md`'s "never commit ... raw datasets ... trained model binaries" rule.
- **Licensing note to confirm before download:** verify the specific PlantVillage mirror/version used allows redistribution of the exact subset the team stores, and record the source URL and license in this file once the subset is picked.
