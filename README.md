# RealFarm — Remote Farming Experience Platform

> Working title. This repository is the implementation skeleton for a graduation project that connects a game-like digital farm with real agricultural plots, real farmers, IoT automation, and real harvest ownership.

## Product idea

A player leases a real plot from the platform, selects an allowed crop, follows the crop through a 2D farm interface, requests selected care actions, and receives the harvest produced by that plot. Safe actions may be automated by IoT. Manual actions are converted into work orders for real farm operators.

The system is **not** a farming simulator whose actions always happen instantly. It is a managed agricultural service with game-like interaction.

## Core value

The main contribution is the controlled link between:

1. a player's action in the digital interface;
2. agronomic policy validation;
3. an automated command or a human work order;
4. verifiable evidence from the real farm;
5. harvest ownership and traceability.

## Repository status

This repository is a documentation-first skeleton. It intentionally contains module boundaries, contracts, rules, and placeholders before implementation starts.

## Start here

Developers and AI agents should read files in this order:

1. [`AGENTS.md`](AGENTS.md)
2. [`docs/00_PROJECT_CONTEXT.md`](docs/00_PROJECT_CONTEXT.md)
3. [`docs/01_SCOPE_AND_NON_GOALS.md`](docs/01_SCOPE_AND_NON_GOALS.md)
4. [`docs/02_BUSINESS_RULES.md`](docs/02_BUSINESS_RULES.md)
5. [`docs/03_ARCHITECTURE.md`](docs/03_ARCHITECTURE.md)
6. The README inside the module being changed
7. Relevant ADRs in [`docs/adr/`](docs/adr/)

A Vietnamese project summary is available at [`docs/PROJECT_SUMMARY_VI.md`](docs/PROJECT_SUMMARY_VI.md).

## Proposed MVP stack

- Web/PWA: React + TypeScript
- 2D farm view: Phaser 3 embedded in React
- Backend: FastAPI modular monolith
- AI: separate Python service only for features that reach MVP readiness
- Data: PostgreSQL with TimescaleDB for telemetry
- IoT: ESP32, MQTT, gateway, and a mandatory simulator
- Media: object storage or local development storage
- Deployment: Docker Compose
- Blockchain: optional extension, not required for the first vertical slice

See [`docs/03_ARCHITECTURE.md`](docs/03_ARCHITECTURE.md) for the reasoning.
