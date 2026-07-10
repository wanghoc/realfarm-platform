# API Guidelines

## Resource groups

Proposed route groups:

```text
/api/v1/auth
/api/v1/plots
/api/v1/crops
/api/v1/service-packages
/api/v1/leases
/api/v1/crop-cycles
/api/v1/player-action-requests
/api/v1/work-orders
/api/v1/telemetry
/api/v1/automation-commands
/api/v1/incidents
/api/v1/harvests
/api/v1/deliveries
/api/v1/traceability
/api/v1/admin
```

## Example state-changing endpoints

```text
POST /api/v1/leases/{lease_id}/activate
POST /api/v1/crop-cycles/{cycle_id}/confirm-planting
POST /api/v1/player-action-requests
POST /api/v1/player-action-requests/{request_id}/cancel
POST /api/v1/work-orders/{work_order_id}/accept
POST /api/v1/work-orders/{work_order_id}/start
POST /api/v1/work-orders/{work_order_id}/complete
POST /api/v1/harvests/{harvest_id}/confirm
```

## Response behavior

- `200`: successful query or idempotent command result.
- `201`: new resource created.
- `202`: accepted for asynchronous processing.
- `400`: malformed request.
- `401`: unauthenticated.
- `403`: authenticated but not authorized.
- `404`: resource absent or intentionally hidden.
- `409`: invalid state transition or resource conflict.
- `422`: domain validation failure.
- `503`: temporary integration unavailable when no graceful fallback exists.

Asynchronous operations should return a resource with a status rather than a vague success message.
