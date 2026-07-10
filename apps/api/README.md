# API Application

FastAPI modular monolith.

## Planned modules

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

Each module should contain domain, application, infrastructure, API, and tests as needed. Do not create empty layers mechanically; add them when behavior exists.

## Boundary rule

No module may directly depend on another module's database model. Use application interfaces, public read models, or domain events.
