# Acceptance Tests — MVP Vertical Slice (Aggregated)

> Week 2 deliverable for issue #8 (`role:bao`). This is the **single aggregated view** of
> the team's acceptance tests, organized around the one MVP vertical slice in
> `docs/01_SCOPE_AND_NON_GOALS.md`. It collects the three role-owned acceptance sets
> (UI / lease-harvest / telemetry-automation) and maps every scenario onto a step of the
> slice, so gaps are visible.
>
> Read alongside: `docs/01_SCOPE_AND_NON_GOALS.md`, `docs/09_VALIDATION_STRATEGY.md`,
> `docs/06_USER_JOURNEYS.md`, `docs/19_STATE_VOCABULARY.md`, and the source acceptance
> documents linked in §2.

Normative keywords `MUST`, `SHOULD`, and `MAY` follow `docs/02_BUSINESS_RULES.md`.

## 1. The slice this must prove

From `docs/01_SCOPE_AND_NON_GOALS.md`, a successful demo shows one unbroken flow:

```text
S1 Plot lease
S2 Crop selection
S3 Crop-cycle activation
S4 Telemetry / simulator update
S5 Player action request
S6 Policy decision
S7 Automated command OR farmer work order
S8 Completion evidence
S9 Harvest record
S10 Player harvest entitlement
```

Per `docs/09_VALIDATION_STRATEGY.md`, this repository keeps **no committed automated test
tree**. These scenarios are Given/When/Then specifications of observable behavior, checked
by the manual smoke flow and, where noted, by contract CI — not by `pytest` files.

## 2. Sources being aggregated

Issue #8 asks for the acceptance tests of three roles to be gathered into one file and
reviewed against scope. Current state of the three sources:

| Role | View | Source | Status |
|---|---|---|---|
| **Khoa** (#7) | Telemetry & automation | [`docs/18_ACCEPTANCE_TESTS_TELEMETRY_AUTOMATION.md`](18_ACCEPTANCE_TESTS_TELEMETRY_AUTOMATION.md) | **Delivered** — scenarios T-01…T-06, A-01…A-09 |
| **Thái** (#5) | UI / player-facing | issue #5 AC "viết acceptance test (mô tả) — góc nhìn UI" | **Not yet written** — §4 is a structured placeholder |
| **Học** (#6) | Lease & harvest | issue #6 AC "viết acceptance test — góc nhìn lease/harvest" | **Not yet written** — §5 is a structured placeholder |

This file is the durable home for all three. When Thái and Học deliver, their scenarios
drop into §4 and §5 and the traceability table in §3 fills in. Tracking of the two
missing sets is proposed as a shared coordination issue (see `PR_TICKET_8.md`).

## 3. Traceability — slice step to scenario

Each slice step should be covered by at least one acceptance scenario. `TBD` marks a step
whose owner has not yet written the scenario.

| Step | Behavior | Owner view | Scenario(s) | Status |
|---|---|---|---|---|
| S1 | Plot lease request & activation | Học (lease) | `L-*` | TBD (#6) |
| S2 | Crop selection from approved catalog | Học / Thái | `L-*` / `U-*` | TBD |
| S3 | Crop-cycle activation | Học (lease) | `L-*` | TBD (#6) |
| S4 | Telemetry / simulator update ingested & served | Khoa | T-01, T-02, T-03, T-04, T-05, T-06 | Specified (blocked by simulator drift) |
| S5 | Player submits an action request | Thái (UI) + Khoa | `U-*`, A-01 | Partly specified |
| S6 | Policy returns one outcome + reason | Khoa | A-01, A-08 | Specified |
| S7a | Accepted → exactly one automation command | Khoa | A-01, A-02, A-03, A-04, A-05, A-06, A-07 | Specified |
| S7b | Accepted → farmer work order | Khoa / Học | A-08, `L-*` | Partly specified |
| S8 | Completion evidence recorded | Học (work/harvest) | `L-*` | TBD (#6) |
| S9 | Harvest record linked to cycle & lease | Học (harvest) | `L-*` | TBD (#6) |
| S10 | Player harvest entitlement shown honestly | Thái (UI) + Học | `U-*`, `L-*` | TBD |

Coverage today is strongest in the middle of the slice (S4–S7, Khoa) and thinnest at the
ends (S1–S3 lease, S8–S10 harvest/UI), which is expected: those are Học's and Thái's
week-2 deliverables and are not written yet.

## 4. UI / player-facing scenarios — Thái (#5) — PLACEHOLDER

> To be filled by Thái. Suggested scenarios so the aggregated file already has the right
> slots (IDs `U-01`, `U-02`, …). The UI boundary rule (`frontend/README.md`) applies to
> all of them: the UI MUST NOT treat its own state as the source of truth, and MUST show
> `accepted | scheduled | rejected | expired | completed` honestly
> (`docs/19_STATE_VOCABULARY.md` §5, `AGENTS.md` §7).

- **U-01 — Lease onboarding flow (S1–S3):** a player browses plots, requests a lease, and
  sees activation state come from the API, not optimistic UI state.
- **U-02 — Submitting an action request (S5):** the action panel sends a
  `player-action-request.v1` payload; the UI shows a pending state until the backend
  returns an outcome.
- **U-03 — Displaying a policy outcome (S6):** each of the six policy outcomes maps to one
  of the five player display states per `docs/19_STATE_VOCABULARY.md` §5
  (`requires_expert_review` → `scheduled`).
- **U-04 — Never claiming an unconfirmed action (S7):** a command that is not yet
  acknowledged MUST NOT be shown as completed (mirrors A-05 from the UI side).
- **U-05 — Harvest summary & entitlement (S9–S10):** the player sees a harvest summary
  bound to their own lease and cannot see another player's plot.

## 5. Lease & harvest scenarios — Học (#6) — PLACEHOLDER

> To be filled by Học. Suggested scenarios (IDs `L-01`, `L-02`, …) covering the slice ends
> that Khoa's telemetry set does not reach.

- **L-01 — A lease activates against an available plot (S1):** requesting a lease on a free
  plot moves it to active; a second player cannot lease the same plot.
- **L-02 — Crop selection locks (S2–S3):** after crop-cycle activation, crop selection is
  immutable (ties to `request_crop_change` → `rejected` in `docs/15_ACTION_CATALOG.md`).
- **L-03 — Work order completion requires evidence (S8):** completing a work-order item
  without before/after evidence is blocked unless an explicit, attributed exception is
  recorded (`docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md` §4.3).
- **L-04 — Harvest record links to the right lease (S9):** a `harvest-record.v1` is bound
  to the correct `cropCycleId` and `leaseId`; weights are non-negative and
  `acceptedWeightKg + rejectedWeightKg <= totalWeightKg`.
- **L-05 — Entitlement follows the lease (S10):** only `safetyStatus = accepted` produce is
  released to the player who held the lease.

## 6. Telemetry & automation scenarios — Khoa (#7) — DELIVERED

The full, authoritative set lives in
[`docs/18_ACCEPTANCE_TESTS_TELEMETRY_AUTOMATION.md`](18_ACCEPTANCE_TESTS_TELEMETRY_AUTOMATION.md).
It is not duplicated here to avoid two copies drifting apart. Summary for the slice map:

- **Telemetry ingest (S4):** T-01 store & serve a valid measurement; T-02 replay dedup;
  T-03 quarantine suspicious readings; T-04 reject malformed payloads without killing the
  consumer; T-05 unit must match sensor type; T-06 authorization on read.
- **Automation (S6–S7):** A-01 one safe request → one command; A-02 idempotency;
  A-03 server-side duration cap; A-04 ack → final state; A-05 timeout;
  A-06 watchdog stop; A-07 emergency overrides preference; A-08 restricted actuator →
  expert review; A-09 every command records its source.

Several are blocked today by the simulator payload/behavior drift documented in
`backend/services/simulator/README.md` and guarded by the `iot-measurement.v1` contract.

## 7. Review against scope (`docs/01_SCOPE_AND_NON_GOALS.md`)

Checking the aggregated scenarios against the MVP success criteria:

| Scope success criterion | Covered by | Verdict |
|---|---|---|
| Full vertical flow demonstrable via the simulator | S1–S10 map above | Partial — middle covered, ends TBD (#5, #6) |
| Real hardware can replace the simulator without changing contracts | gateway/simulator same contract; A-04/A-05; `iot-measurement.v1` | Specified |
| A player cannot bypass agronomic safety rules | A-03, A-07, A-08; `docs/15_ACTION_CATALOG.md` Category C | Specified |
| Every manual action traces to a work order | S7b, A-09, L-03 | Partial — L-03 (Học) TBD |
| System recovers from AI / MQTT / blockchain unavailability | T-04, A-05, A-06 | Specified (AI/blockchain recovery not yet a scenario) |
| Harvest record linked to the correct player lease and crop cycle | S9, L-04, `harvest-record.v1` | Specified in contract; L-04 (Học) TBD |

**Out-of-scope check:** no scenario asks for direct device control, player-set chemical
dosage, guaranteed yield, or the other non-goals in
`docs/01_SCOPE_AND_NON_GOALS.md` — the restricted actions (`request_treatment`,
`request_early_harvest`, `request_crop_change`) are covered precisely to prove they are
**refused** (A-08 and the Category C rows of `docs/15_ACTION_CATALOG.md`).

## 8. Open items

1. Thái's UI scenarios (§4) and Học's lease/harvest scenarios (§5) are the two missing
   sources; without them S1–S3 and S8–S10 stay TBD. Proposed to track in a shared
   coordination issue (see `PR_TICKET_8.md`).
2. AI availability/recovery (scope criterion 5) has no acceptance scenario yet — belongs
   with the AI MVP candidate work (`docs/adr/0005-ai-leaf-disease-mvp-candidate.md`, Bảo).
3. `docs/09_VALIDATION_STRATEGY.md` rules out a committed test tree; the failure-path
   scenarios (A-05, A-06) remain painful to check by hand. Whether the Weeks 7-8 IoT flows
   justify a simulator-driven scenario runner is an open question already raised in
   `docs/18_ACCEPTANCE_TESTS_TELEMETRY_AUTOMATION.md` §6.
