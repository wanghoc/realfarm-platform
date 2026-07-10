# Proposed 16-Week Roadmap

This roadmap starts implementation earlier than the original document-heavy plan.

## Weeks 1–2 — Product and domain lock

- confirm plot unit and lease policy;
- confirm harvest ownership and failure compensation;
- choose MVP crop;
- define action catalog;
- define operator workflow;
- approve scope and non-goals;
- create initial UI wireframes and contracts.

Deliverable: reviewed domain rules and vertical-slice acceptance test.

## Weeks 3–4 — Repository and foundation

- bootstrap web, API, database, simulator, and Docker Compose;
- authentication and roles;
- farm, plot, crop catalog, and lease skeleton;
- CI checks;
- initial migrations.

Deliverable: player can authenticate and view available plots.

## Weeks 5–6 — Lease and crop-cycle vertical slice

- lease request/activation;
- crop selection;
- plot assignment;
- crop-cycle state machine;
- operator planting confirmation.

Deliverable: active player plot appears in a basic non-game dashboard.

## Weeks 7–8 — Telemetry and automation

- MQTT simulator;
- telemetry persistence;
- realtime updates;
- policy engine;
- irrigation command and acknowledgement;
- watchdog.

Deliverable: safe watering request works end to end.

## Weeks 9–10 — Human work orchestration

- player action requests;
- work-order batching and assignment;
- operator portal;
- evidence upload;
- care timeline.

Deliverable: manual inspection request works end to end.

## Weeks 11–12 — Game-like Digital Twin

- Phaser farm map;
- plot ownership visualization;
- growth stages;
- request interactions;
- timeline and camera snapshot;
- notification feedback.

Deliverable: MVP vertical slice in game-like UI.

## Weeks 13–14 — Harvest and traceability

- harvest recording;
- accepted/rejected quantities;
- harvest entitlement;
- pickup/delivery request;
- QR timeline;
- optional AI baseline integration.

Deliverable: complete lease-to-harvest demonstration.

## Weeks 15–16 — Hardening and defense

- end-to-end tests;
- security and authorization review;
- real hardware substitution test;
- performance checks;
- documentation, report, slides, and backup demo;
- optional blockchain hash anchoring only if core MVP is stable.

Deliverable: defendable, repeatable demonstration.
