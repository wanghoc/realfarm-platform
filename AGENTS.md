# AGENTS.md

This file defines mandatory working rules for AI coding agents and human developers.

## 1. Context loading order

Before modifying code, read:

1. `docs/00_PROJECT_CONTEXT.md`
2. `docs/01_SCOPE_AND_NON_GOALS.md`
3. `docs/02_BUSINESS_RULES.md`
4. `docs/03_ARCHITECTURE.md`
5. `docs/04_DOMAIN_MODEL.md`
6. the target module's `README.md`
7. related ADRs in `docs/adr/`

Do not rely on chat memory when repository documentation exists.

## 2. Product invariants

The following rules must never be bypassed:

- A player leases a real plot, not a virtual-only asset.
- The accepted harvest from the assigned crop cycle belongs to the player under the lease policy.
- Player actions are requests, not unrestricted actuator commands.
- Emergency automation and safety policies override player preferences.
- Chemical treatment, pesticide use, and destructive actions require an authorized farm operator or expert.
- Every manual farm task must be traceable to a work order.
- Completing a manual work order requires evidence or an explicit evidence exception.
- Plot replacement must be transparent; history must never be silently rewritten.
- A plot can have at most one active lease and one active crop cycle at a time.
- Hardware unavailability must not block development; the simulator is a first-class component.

## 3. Change protocol

For every task:

1. Restate the target behavior in one or two sentences.
2. Inspect existing files before creating new abstractions.
3. Identify affected modules and business rules.
4. Implement the smallest coherent change.
5. Add or update tests.
6. Update contracts and documentation when behavior changes.
7. Report changed files, assumptions, and unresolved risks.

Do not perform broad refactors unless the task explicitly requires them.

## 4. Git and GitHub rules

- Never push directly to `main`.
- Use short-lived branches:
  - `feat/<issue>-<name>`
  - `fix/<issue>-<name>`
  - `docs/<issue>-<name>`
  - `refactor/<issue>-<name>`
  - `test/<issue>-<name>`
  - `chore/<issue>-<name>`
- Use Conventional Commits:
  - `feat: add plot lease activation`
  - `fix: reject unsafe watering request`
  - `docs: clarify harvest ownership`
- Keep each commit focused and buildable.
- Do not mix formatting-only changes with behavior changes.
- One pull request should solve one task or one tightly related task group.
- Pull requests require passing tests and at least one reviewer.
- Do not merge, force-push reviewed branches, rewrite shared history, or delete remote branches without explicit approval.
- Never commit secrets, private keys, model binaries, datasets, generated media, or local environment files.

See `CONTRIBUTING.md` for the full workflow.

## 5. Code language and comments

- Source code, identifiers, API fields, database names, comments, commit messages, and PR titles must be in English.
- Business explanations for the team may be written in Vietnamese in dedicated documents.
- Comments explain **why**, constraints, or non-obvious trade-offs. Do not narrate obvious code.
- Public functions and domain services should have concise docstrings when intent is not obvious.

## 6. Backend rules

- Keep the backend a modular monolith until an ADR approves extraction.
- Routes/controllers only validate transport concerns and call application services.
- Domain rules belong in domain/application layers, not in routes or ORM models.
- Do not expose ORM entities directly through APIs.
- Use typed request/response schemas.
- Use UTC internally.
- Use migrations for every database schema change.
- Use explicit transactions for multi-step state changes.
- Use durable jobs for work that must survive restarts.
- Public APIs are versioned under `/api/v1`.
- Validate authorization at the use-case boundary, not only in the UI.

## 7. Frontend rules

- Use TypeScript strict mode.
- Organize code by feature, not only by technical file type.
- Keep Phaser game state separate from server/domain state.
- The UI must never assume a request was executed until the backend reports an accepted or completed state.
- Every player action must display one of: accepted, scheduled, rejected, expired, or completed.
- Critical actions require confirmation and a human-readable reason.
- Accessibility and responsive layout are required for non-game screens.

## 8. IoT and automation rules

- Player requests must pass through the policy engine.
- The gateway must acknowledge commands and report final device state.
- Commands require idempotency keys.
- Add watchdog limits for actuators.
- Record command source: `automation`, `operator`, `player_request`, or `emergency`.
- Sensor values must include timestamp, device identity, unit, and quality status.
- Invalid or suspicious values are quarantined; they are not silently treated as valid measurements.
- The simulator must implement the same contract as the real gateway.

## 9. AI rules

- AI output is advisory unless an approved business rule explicitly automates a response.
- Every model output includes model version, confidence, timestamp, and input reference.
- Low-confidence predictions require manual review.
- Do not claim accuracy without an evaluation dataset and recorded metrics.
- A baseline model and failure cases must be documented.
- Model files and datasets are not committed to Git unless explicitly approved.

## 10. Blockchain rules

- Blockchain is an optional extension for integrity proof.
- Full records remain off-chain; only hashes and minimal metadata may be anchored.
- Core business operations must continue when the blockchain network is unavailable.
- Never represent blockchain as proof that source data was truthful.
- Do not introduce blockchain dependencies into the MVP core without an ADR.

## 11. Testing requirements

A change is not complete without appropriate tests:

- domain unit tests for business rules;
- integration tests for persistence and queues;
- API contract tests for request/response behavior;
- end-to-end tests for critical user journeys;
- simulator tests for IoT command flows.

Bug fixes require a regression test whenever practical.

## 12. Forbidden actions

AI agents must not:

- invent requirements that conflict with documented rules;
- silently change scope or architecture;
- bypass authorization or safety checks for convenience;
- add new frameworks without documenting the reason;
- run destructive database or Git commands without explicit approval;
- delete documentation because it appears outdated; update it or mark it deprecated;
- mark a task complete while tests or validation are known to fail.
