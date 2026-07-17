# State Vocabulary — Player Actions and Work Orders

> Week 2 deliverable for issue #64 (`role:khoa`). Single reference for every state-like
> value used around a player action request and a work order: which layer it belongs to,
> which document owns it, and how the layers map onto each other.
>
> Read alongside: `docs/02_BUSINESS_RULES.md` (Player actions),
> `docs/04_DOMAIN_MODEL.md`, `AGENTS.md` §7, `docs/09_VALIDATION_STRATEGY.md`,
> `docs/15_ACTION_CATALOG.md`, `docs/16_OPERATOR_WORKFLOW.md`, and
> `backend/app/modules/player_actions/api/router.py`.

Normative keywords `MUST`, `SHOULD`, and `MAY` follow `docs/02_BUSINESS_RULES.md`.

## At a glance

- **Reported (#64):** at least three documents give different value sets for "the state of
  a player action," and nothing detects when they drift apart.
- **Finding:** the values do **not** conflict. They belong to **three layers** that were
  never named (table below). Comparing a value from one layer against a value from another
  only *looks* like a contradiction.
- **Fixed here:** named the three layers, gave each one authority document, wrote the
  outcome → display mapping (§5), and corrected one sequence diagram in
  `docs/04_DOMAIN_MODEL.md` that drew mutually-exclusive outcomes as a sequence.
- **Still needs a decision (not code):** §6.1 `requires_expert_review` has no player
  display value; §6.2 `rejected` is missing from `work-order.v1`. Both wait on @wanghoc.

| Layer | Answers | Values | Authority document |
|---|---|---|---|
| **Policy decision outcome** | What did the policy decide about this request? | 6 | `docs/02_BUSINESS_RULES.md` |
| **Request lifecycle state** | Where is this request row in its life? | 11 | `docs/04_DOMAIN_MODEL.md` |
| **Player display status** | What does the player see in the UI? | 5 | `AGENTS.md` §7 |

The rest of this document is the detail behind that table: one section per layer (§2–§4),
the mapping (§5), the open questions (§6), and the commands that re-check it all (§7).

## 1. Why this document exists

Issue #64 reported that several documents describe "the state of a player action" with
different value sets, and that nothing detects divergence.

Auditing every occurrence showed the values do **not** conflict. They belong to the three
layers named in the table at the top of this document, so a reader comparing two of them
across layers sees a contradiction that is not there.

Within each layer, every source already agrees. The gaps are that the layers were not
named, that the mapping between them was never written down, and that one diagram in
`04_DOMAIN_MODEL.md` renders exclusive outcomes as a sequence.

## 2. Layer 1 — Policy decision outcome

**Authority: `docs/02_BUSINESS_RULES.md`** ("Player actions"), which states the policy
result MUST be one of six values. `PolicyDecision.result` in
`backend/app/modules/player_actions/api/router.py` is the executable copy of that rule,
not a competing definition — business rules decide, code implements.

| Value | Meaning |
|---|---|
| `accepted_for_automation` | Safe to execute automatically now |
| `accepted_for_work_order` | Needs a human on-site |
| `scheduled` | Valid but deferred to a future window |
| `rejected` | Not permitted or unsafe right now |
| `requires_expert_review` | Risk or ambiguity needs an agronomy expert |
| `expired` | Request TTL passed before evaluation |

These are **mutually exclusive**. Exactly one is returned per evaluation, always with a
human-readable reason (`docs/02_BUSINESS_RULES.md`, ADR-0003).

Sources currently in agreement: `docs/02_BUSINESS_RULES.md` (authority),
`player_actions/api/router.py` (`Literal[...]`), `docs/15_ACTION_CATALOG.md` §2.

## 3. Layer 2 — Request lifecycle state

**Authority: `docs/04_DOMAIN_MODEL.md`** (`PlayerActionRequest`).

A request row lives longer than one decision. Its lifecycle **contains** the six
outcomes as a middle stage:

```text
submitted → evaluating → <one policy outcome> → completed | failed | cancelled
```

- `submitted`, `evaluating` — before a decision exists.
- The six outcomes of §2 — the decision itself, recorded on the row.
- `completed` — the accepted work actually finished (the automation command succeeded, or
  the work-order item was verified).
- `failed` — the request was accepted but execution did not succeed.
- `cancelled` — the player withdrew it (`POST /player-action-requests/{id}/cancel`).

`completed`, `failed`, and `cancelled` are **not** policy outcomes: a policy never
returns them. They describe what happened after a decision. No code models this layer
yet; `player_actions/api/router.py` currently exposes only the decision.

## 4. Layer 3 — Player display status

**Authority: `AGENTS.md` §7**, which requires that every player action display one of
five values. `docs/09_VALIDATION_STRATEGY.md` (manual smoke check 5) checks exactly this
layer, and agrees with it.

| Value | Player reads it as |
|---|---|
| `accepted` | We took it and are acting on it |
| `scheduled` | Valid, but it will happen later |
| `rejected` | We will not do this — with a reason |
| `expired` | Too late; resubmit if you still want it |
| `completed` | Done |

This layer is deliberately smaller and blunter than the other two. It follows the same
principle as customer-safe work-order status (`docs/16_OPERATOR_WORKFLOW.md` §8): the
player sees the outcome, not the internal machinery.

`accepted` is **not** missing from the code. It is a display value, and no display layer
is implemented yet.

## 5. Mapping — outcome → display

This is the table that was missing. Every outcome MUST map to exactly one display value,
because `AGENTS.md` §7 allows no sixth option.

| Policy outcome (§2) | Player display (§4) | Note |
|---|---|---|
| `accepted_for_automation` | `accepted` | → `completed` once the command succeeds |
| `accepted_for_work_order` | `accepted` | → `completed` once the item is verified |
| `scheduled` | `scheduled` | re-evaluated in the next window |
| `requires_expert_review` | `scheduled` | **see §6.1 — needs confirmation** |
| `rejected` | `rejected` | reason MUST be shown |
| `expired` | `expired` | player may resubmit |

And lifecycle → display:

| Lifecycle state (§3) | Player display |
|---|---|
| `submitted`, `evaluating` | `scheduled` (no decision yet) |
| `completed` | `completed` |
| `failed` | `rejected` (with the failure reason) |
| `cancelled` | not shown as an action state; the request disappears from the active list |

The reason string carries what the display value cannot. `AGENTS.md` §7 already requires
a human-readable reason for critical actions, which is what keeps `scheduled` from being
misleading for an expert review.

## 6. Open questions

### 6.1 `requires_expert_review` has no natural display value — needs a decision

`AGENTS.md` §7 permits five display values, and `requires_expert_review` matches none of
them. §5 maps it to `scheduled` because that is the only non-terminal option, but a
player told "scheduled" is not told that a human expert is now involved — which matters
for exactly the actions where it fires: pruning, chemical treatment
(`docs/15_ACTION_CATALOG.md` §4.3).

Two options:

1. **Keep the mapping to `scheduled`**, and rely on the reason string to say an expert is
   reviewing. No rule change.
2. **Add a sixth display value** (e.g. `under_review`) to `AGENTS.md` §7. Clearer for the
   player, but it edits the mandatory rules file and the frontend must handle it.

This document assumes option 1 until decided. Frontend owner (Thái) and @wanghoc.

### 6.2 `rejected` is missing from `work-order.v1` — still blocking

Unchanged from `docs/16_OPERATOR_WORKFLOW.md` §9.6 and issue #64: the `status` enum in
`packages/contracts/schemas/work-order.v1.json` is
`draft|assigned|accepted|in_progress|completed|verified|blocked|cancelled` and has no
`rejected`, while `docs/04_DOMAIN_MODEL.md` lists it.

Note the `assigned → draft` alternative **loses the record that a specific operator
declined the task**, which works against `AGENTS.md` §2 ("Every manual farm task must be
traceable to a work order"). Widening the contract enum preserves it.

Not decided here — needs @wanghoc, before the `work_orders` migration.

### 6.3 Nothing enforces this document

There is no automated guard, by design: `docs/09_VALIDATION_STRATEGY.md` states the
repository keeps no committed automated test tree. The checks in §7 are manual and must
be re-run whenever a state value is added.

## 7. How to verify this document is still true

Run these from the repository root. Each should produce the result described.

```bash
# 1. The six policy outcomes, from the authority (docs/02_BUSINESS_RULES.md)
sed -n '/The policy result MUST be one of/,/human-readable reason/p' docs/02_BUSINESS_RULES.md

# 2. The executable copy must list the same six
sed -n '/class PolicyDecision/,/reason: str/p' backend/app/modules/player_actions/api/router.py

# 3. Every display-layer occurrence must be the same five values
grep -rn "one of: accepted\|state is accepted" AGENTS.md docs/

# 4. No state value may exist outside a layer named in this document
grep -rn "requires_expert_review" --include='*.py' --include='*.md' --include='*.json' .
```

If (1) and (2) disagree, the code is wrong — `docs/02_BUSINESS_RULES.md` decides.
If a value appears in (4) that §2–§4 do not name, this document is out of date.
