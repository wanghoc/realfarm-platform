# Scope and Non-Goals

## MVP objective

Deliver one complete vertical slice for one greenhouse, two or three real plots, and one crop type such as tomato.

A successful demo must show:

```text
Plot lease
→ Crop selection
→ Crop-cycle activation
→ Telemetry/simulator update
→ Player action request
→ Policy decision
→ Automated command or farmer work order
→ Completion evidence
→ Harvest record
→ Player harvest entitlement
```

## In scope

### Player experience

- account and authentication;
- available plot browsing;
- plot lease request and activation;
- crop selection from an approved catalog;
- 2D digital farm view;
- plot status, growth stage, health summary, and timeline;
- on-demand camera snapshot or limited stream;
- safe player action requests;
- notifications;
- harvest summary;
- pickup or basic delivery request.

### Farm operations

- farm, greenhouse, plot, and crop-cycle management;
- operator task dashboard;
- work-order assignment and batching;
- evidence upload;
- care logs;
- incident reporting;
- harvest weighing and quality acceptance;
- plot replacement workflow.

### IoT and automation

- telemetry ingestion;
- mandatory simulator;
- basic sensors: air temperature/humidity and soil moisture;
- optional light and pH when hardware is ready;
- automated irrigation;
- watchdog and emergency stop;
- command acknowledgement and audit history.

### Traceability

- complete off-chain timeline;
- QR-based read-only view;
- integrity hash;
- optional blockchain anchoring.

### AI

At most one AI feature should be treated as MVP-ready, preferably disease detection with clear confidence and manual-review behavior. Other AI features remain experimental or post-MVP.

## Out of scope for MVP

- native mobile application;
- open-world or multiplayer game;
- unrestricted direct control of devices;
- player-controlled pesticide or fertilizer dosage;
- guaranteed fixed yield;
- marketplace for trading plots or produce;
- multi-farm and national-scale deployment;
- real payment gateway;
- advanced logistics integration;
- production-grade computer vision for yield counting;
- fully automated produce grading;
- multi-organization blockchain network;
- autonomous agronomic treatment decisions.

## MVP success criteria

- A complete vertical flow can be demonstrated without real hardware by using the simulator.
- Real hardware can replace the simulator without changing upper-layer contracts.
- A player cannot bypass agronomic safety rules.
- Every manual action can be traced to a work order.
- The system can recover from temporary AI, MQTT, or blockchain unavailability.
- The harvest record is linked to the correct player lease and crop cycle.
