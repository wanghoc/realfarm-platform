# RealFarm

RealFarm is a remote farming experience platform with real plots, policy-controlled player actions, IoT automation, and harvest traceability.

The repository is organized around two major product areas:

- `backend/` for the FastAPI modular monolith.
- `frontend/` for the React + TypeScript web app.

Documentation, setup guidance, and repository policy live at the same top level as BE and FE so they are easy to find.

## Start here

- [SETUP.md](SETUP.md) for local and Docker setup.
- [docs/03_ARCHITECTURE.md](docs/03_ARCHITECTURE.md) for the system view.
- [docs/02_BUSINESS_RULES.md](docs/02_BUSINESS_RULES.md) for product invariants.
- [docs/04_DOMAIN_MODEL.md](docs/04_DOMAIN_MODEL.md) for the domain aggregates.
- [PROJECT_TREE.md](PROJECT_TREE.md) for the visual structure map.
- [CONTRIBUTING.md](CONTRIBUTING.md) for collaboration rules.

## Top-level layout

```text
realfarm-platform/
- backend/
- frontend/
- docs/
- infra/
- packages/
- scripts/
- templates/
- README.md
- SETUP.md
- AGENTS.md
- CONTRIBUTING.md
- PROJECT_TREE.md
- SECURITY.md
```

## What lives where

- `backend/`: transactional API, business rules, migrations, and modular domain code.
- `backend/services/`: backend-adjacent services such as simulator, gateway, AI service, and firmware.
- `frontend/`: customer and operator web experience.
- `docs/`: project context, architecture, rules, ADRs, and implementation guidance.
- `infra/`: environment and platform support files.
- `packages/`: shared contracts and schemas.
- `scripts/`: helper scripts for local development and maintenance.
- `templates/`: reusable documentation templates.

## Validation model

This repository currently relies on lint, type-check, build, import, and manual smoke checks instead of a committed automated test tree.
