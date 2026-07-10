# Domain Model

## Main aggregates

### Plot

Represents a real physical growing area.

Important state:

- identity and farm location;
- area and capacity;
- operational status;
- supported crops;
- current lease;
- current crop cycle;
- camera and device bindings.

### Lease

Represents the customer's right to use a plot under a service package.

States:

```text
draft
→ pending_payment_or_approval
→ active
→ completed
```

Alternative terminal states:

```text
cancelled
expired
terminated
```

### CropCycle

Represents one crop lifecycle on one plot.

States:

```text
planned
→ planted
→ growing
→ awaiting_harvest
→ harvested
→ closed
```

Alternative states:

```text
failed
cancelled
```

### PlayerActionRequest

Represents player intent, never a direct hardware command.

States:

```text
submitted
→ evaluating
→ accepted_for_automation
→ scheduled
→ completed
```

Alternative states:

```text
accepted_for_work_order
requires_expert_review
rejected
expired
cancelled
failed
```

### WorkOrder

Represents real manual work.

States:

```text
draft
→ assigned
→ accepted
→ in_progress
→ completed
→ verified
```

Alternative states:

```text
rejected
cancelled
blocked
```

### AutomationCommand

Represents a command to an actuator.

States:

```text
created
→ published
→ acknowledged
→ running
→ succeeded
```

Alternative states:

```text
rejected_by_gateway
timed_out
failed
stopped_by_watchdog
cancelled
```

### HarvestBatch

Represents measured produce from a crop cycle.

It stores total weight, accepted weight, rejected weight, quality notes, safety status, and evidence.

### HarvestEntitlement

Connects a harvest batch to the player lease. For MVP, one crop cycle normally maps to one player's entitlement.

## Supporting entities

- Farm
- Greenhouse
- CropCatalogItem
- ServicePackage
- SensorDevice
- ActuatorDevice
- Measurement
- ActionPolicy
- CareLog
- WorkEvidence
- Incident
- ReplacementAssignment
- Notification
- DeliveryOrder
- TraceabilityRecord
- AIInference
