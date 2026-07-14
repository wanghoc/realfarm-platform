# API Application

FastAPI modular monolith.

## Module layout

```text
app/modules/
  auth/
  users/
  farms/
  plots/
  crop_catalog/
  leases/
  crop_cycles/
  telemetry/
  automation/
  player_actions/
  work_orders/
  care_logs/
  incidents/
  harvests/
  deliveries/
  notifications/
  traceability/
  admin/
```

Each module should contain only the layers it needs. Keep domain rules in the module, call them from application services, expose transport adapters through API routers, and add infrastructure code only when the behavior requires it.

## Boundary rule

No module may directly depend on another module's database model. Use application interfaces, public read models, or domain events.

## Supporting services

Backend-owned supporting services live under `services/`:

```text
services/
  simulator/
  gateway/
  firmware/
  ai-service/
```

The simulator is required for local development. Gateway, firmware, and AI service are kept close to the backend because they share automation, telemetry, and integration contracts.
