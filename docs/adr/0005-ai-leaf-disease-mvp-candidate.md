# ADR 0005 — Leaf Disease Classification via Transfer Learning as the AI MVP Candidate

- Status: Proposed

## Context

`apps/ai-service` ([README](../../apps/ai-service/README.md)) names leaf disease classification as the MVP candidate, with required output: model version, confidence, input image reference, evaluation metrics, manual-review threshold, and a retry-safe inference endpoint. The service must not command actuators, must not decide chemical treatment, must not claim production accuracy without evidence, and must not store lease/harvest ownership data ([03_ARCHITECTURE.md](../03_ARCHITECTURE.md#L69), [12_SECURITY_AND_PRIVACY.md](../12_SECURITY_AND_PRIVACY.md#L24)).

The team has no dedicated GPU infrastructure and a short schedule (baseline training targets Tuần 8-9 per [KE_HOACH_16_TUAN_CHI_TIET_VI.md](../KE_HOACH_16_TUAN_CHI_TIET_VI.md#L159)). Training a classifier from scratch is not realistic in that time; a pretrained backbone with transfer learning is required.

## Decision

Adopt transfer learning on a small, CPU-friendly convolutional backbone for the first baseline:

- **Backbone candidates:** MobileNetV2 or EfficientNet-B0 (ImageNet-pretrained), fine-tuned on a leaf-disease dataset. MobileNetV2 is the default choice for the first baseline because inference latency and CPU cost matter more at MVP stage than the last percentage points of accuracy; EfficientNet-B0 is the fallback if accuracy proves insufficient.
- **Training data source:** PlantVillage (public dataset), scoped to a subset of crops matching the crop catalog Học/Khoa are defining for the MVP. Real farm camera images are explicitly out of scope for training until documented approval exists, per [12_SECURITY_AND_PRIVACY.md:24](../12_SECURITY_AND_PRIVACY.md#L24).
- **Inference output contract (draft, to be formalized as a schema in Tuần 2):**
  - `detectionId`
  - `imageRef`
  - `modelVersion`
  - `predictedClass`
  - `confidence`
  - `status` (`pending` | `needs_review` | `confirmed`) — anything below the manual-review threshold is `needs_review`, never auto-escalated to an action.
- **Retry behavior:** inference runs as a database-backed durable job, matching the durable-job pattern already used for the platform ([03_ARCHITECTURE.md:84](../03_ARCHITECTURE.md#L84)), not a new queue platform.
- **Decision boundary:** the model output is a signal for a work order or expert review, never a direct instruction to an actuator and never an automatic chemical-treatment decision. This mirrors the policy-controlled action pattern in [ADR 0003](0003-policy-controlled-player-actions.md).

## Consequences

- No GPU procurement needed for the MVP baseline; training and inference can run on CPU, at the cost of a longer inference time than a heavier model would give.
- Because training data is PlantVillage (not local farm images), early accuracy numbers describe PlantVillage performance, not proven field performance on the platform's actual crops/cameras — any accuracy claim must state this scope explicitly, per the non-goal "claim production accuracy without evidence."
- A new contract schema (e.g. `disease-detection-result.v1`) will need to be proposed during Tuần 2 contract finalization; none of the four existing schemas model AI detection output today (see [apps/ai-service/DATA_PLAN.md](../../apps/ai-service/DATA_PLAN.md) for the schema review and data-source plan).
- Using real farm camera images later (Tuần 8+) requires a documented approval step before they can be used for training, not just for inference.
