# Project Tree

```text
realfarm-platform/
|- backend/
|  |- app/
|  |  |- core/
|  |  `- modules/
|  |     |- auth/
|  |     |- users/
|  |     |- farms/
|  |     |- plots/
|  |     |- crop_catalog/
|  |     |- leases/
|  |     |- crop_cycles/
|  |     |- telemetry/
|  |     |- automation/
|  |     |- player_actions/
|  |     |- work_orders/
|  |     |- care_logs/
|  |     |- incidents/
|  |     |- harvests/
|  |     |- deliveries/
|  |     |- notifications/
|  |     |- traceability/
|  |     `- admin/
|  |- services/
|  |  |- ai-service/
|  |  |- firmware/
|  |  |- gateway/
|  |  `- simulator/
|  `- alembic/
|- frontend/
|  `- src/
|     |- features/
|     |  |- auth/
|     |  |- dashboard/
|     |  |- farm/
|     |  |- operator/
|     |  `- plots/
|     `- shared/
|        |- api/
|        |- components/
|        |- layouts/
|        |- pages/
|        `- store/
|- docs/
|  |- 00_PROJECT_CONTEXT.md
|  |- 01_SCOPE_AND_NON_GOALS.md
|  |- 02_BUSINESS_RULES.md
|  |- 03_ARCHITECTURE.md
|  |- 04_DOMAIN_MODEL.md
|  |- 05_ACTORS_AND_PERMISSIONS.md
|  |- 06_USER_JOURNEYS.md
|  |- 07_DATA_MODEL_GUIDE.md
|  |- 08_CODING_STANDARDS.md
|  |- 09_VALIDATION_STRATEGY.md
|  |- 10_ROADMAP_16_WEEKS.md
|  |- 11_CHANGES_FROM_ORIGINAL_PROPOSAL.md
|  |- 12_SECURITY_AND_PRIVACY.md
|  |- 13_ASSUMPTIONS_AND_OPEN_QUESTIONS.md
|  |- 14_GLOSSARY.md
|  |- AI_AGENT_PLAYBOOK.md
|  |- API_GUIDELINES.md
|  |- PROJECT_SUMMARY_VI.md
|  `- adr/
|     |- 0001-modular-monolith.md
|     |- 0002-plot-based-ownership.md
|     |- 0003-policy-controlled-player-actions.md
|     |- 0004-blockchain-optional-extension.md
|     `- README.md
|- infra/
|  |- blockchain/
|  |- database/
|  |- mqtt/
|  `- README.md
|- packages/
|  |- contracts/
|  `- ui/
|- scripts/
|- templates/
|- README.md
|- SETUP.md
|- AGENTS.md
|- CONTRIBUTING.md
|- PROJECT_TREE.md
`- SECURITY.md
```

## Notes

- `backend/` is the largest transactional codebase.
- `frontend/` owns the player and operator experience.
- `docs/`, `README.md`, and `SETUP.md` sit at the same root level as the two application areas.
- Validation guidance lives in `docs/09_VALIDATION_STRATEGY.md`.
