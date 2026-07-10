# User Journeys

## Journey A — Lease and plant

1. Player opens available plots.
2. System shows plot size, supported crops, expected duration, price placeholder, and availability.
3. Player selects a plot and service package.
4. Player selects an allowed crop.
5. System validates availability and compatibility.
6. Admin or automated workflow approves the lease.
7. Crop cycle is created in `planned`.
8. Operator confirms planting.
9. Crop cycle moves to `planted`, then `growing`.
10. Digital Twin displays the assigned plot.

## Journey B — Request watering

1. Player chooses "Request extra watering."
2. System creates `PlayerActionRequest`.
3. Policy engine evaluates soil moisture, recent irrigation, crop stage, weather conditions, and device safety.
4. System either:
   - creates an automation command;
   - schedules the request;
   - rejects it with a reason.
5. Gateway acknowledges execution.
6. Timeline records actual duration and outcome.
7. Player receives a result notification.

## Journey C — Request manual inspection

1. Player requests pest inspection.
2. System validates package limits and request timing.
3. Request becomes a work-order item.
4. Compatible requests are batched.
5. Operator completes inspection and uploads evidence.
6. Expert review is triggered when needed.
7. Player sees the customer-safe result.

## Journey D — Crop incident

1. Sensor, AI, operator, or player reports a problem.
2. System creates an incident.
3. Operator or expert assesses severity.
4. System applies treatment, monitors, replaces, or closes the crop cycle.
5. Player receives a transparent update.
6. Compensation or replacement is recorded when applicable.

## Journey E — Harvest and delivery

1. Crop cycle reaches `awaiting_harvest`.
2. Operator harvests and records weights.
3. Unsafe or rejected produce is separated.
4. System creates the player's harvest entitlement.
5. Player selects pickup or delivery.
6. Produce is packed and labeled.
7. Delivery or pickup is confirmed.
8. Crop cycle and lease are completed.
