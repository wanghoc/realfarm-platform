# README Consistency Review — Week 2

> Week 2 deliverable for issue #8 (`role:bao`). A cross-check of every README and the
> structure map for internal consistency: layout, module lists, naming, and cross-file
> references. Fixes that were safe to make directly are applied in this branch; items
> that belong to another owner are listed for follow-up.

## 1. Scope of the review

Files checked:

| File | Verdict |
|---|---|
| `README.md` (root) | consistent (one minor note, §3) |
| `PROJECT_TREE.md` | **fixed** — docs/ list was stale (§2) |
| `backend/README.md` | consistent; module list matches `PROJECT_TREE.md` |
| `frontend/README.md` | consistent; feature folders match the tree |
| `backend/services/simulator/README.md` | consistent; documents its own contract drift honestly |
| `backend/services/gateway/README.md` | consistent; correctly marked "not implemented yet" |
| `backend/services/firmware/README.md` | consistent |
| `backend/services/ai-service/README.md` | consistent |
| `infra/README.md` | consistent — all six concerns (`database`, `mqtt`, `media`, `blockchain`, `observability`, `docker`) exist on disk |
| `infra/blockchain|database|mqtt/README.md` | consistent |
| `packages/contracts/README.md` | **updated** in this branch (schemas, examples, validator) |
| `scripts/README.md` | consistent |
| `docs/adr/README.md` | consistent |

## 2. Fixed in this branch

**`PROJECT_TREE.md` docs/ list was out of date.** It stopped at `14_GLOSSARY.md` and the
four original ADRs. Added the files that have since landed so the map matches the tree:

- `15_ACTION_CATALOG.md`, `16_OPERATOR_WORKFLOW.md`,
  `17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md`,
  `18_ACCEPTANCE_TESTS_TELEMETRY_AUTOMATION.md`, `19_STATE_VOCABULARY.md`;
- `CONTRIBUTOR_WORKFLOW.md`, `KE_HOACH_16_TUAN_CHI_TIET_VI.md`;
- `adr/0005-ai-leaf-disease-mvp-candidate.md`;
- `wireframes/player-states.md`.

## 3. Notes / follow-ups for other owners

These are consistency gaps found during the review that are **not** README files, or that
belong to another module owner, so they are recorded here rather than edited unilaterally:

1. **`apps/` naming drift in `docs/KE_HOACH_16_TUAN_CHI_TIET_VI.md`.** The repository
   pivoted to `backend/` + `frontend/` + `backend/services/*` (see root `README.md` and
   `PROJECT_TREE.md`), but the 16-week plan still refers to `apps/web`, `apps/api`,
   `apps/gateway`, `apps/simulator`, `apps/firmware`, `apps/ai-service`. Recommend the
   plan's owner update those paths in a docs pass. (Same pivot note applies to any
   ticket-4 material still under `apps/ai-service/`, which is unmerged and out of scope
   for this branch.)

2. **`work-order.v1.status` contract drift.** `docs/04_DOMAIN_MODEL.md` and
   `docs/16_OPERATOR_WORKFLOW.md` use a `rejected` state absent from
   `packages/contracts/schemas/work-order.v1.json`
   (`docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md` §4.1). Owner decision (Học):
   widen the enum or drop the domain state. The contract keeps the narrower set for now
   and `packages/contracts/README.md` documents it.

3. **Root `README.md` "What lives where"** describes `packages/` as "shared contracts and
   schemas"; `packages/ui/` also exists (currently an empty `.gitkeep` placeholder).
   Left as-is — accurate enough while `ui` is empty; revisit when `packages/ui` gets
   content.

## 4. Result

No contradictions remain between the README files and the actual tree after the
`PROJECT_TREE.md` fix. The two open drifts (§3.1, §3.2) are tracked to their owners and,
for the contract drift, additionally guarded by the contracts CI
(`work-order.v1.invalid.json`).
