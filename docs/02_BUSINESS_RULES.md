# Business Rules

Normative keywords `MUST`, `SHOULD`, and `MAY` indicate requirement strength.

## Plot and lease

- A plot MUST represent a real, identifiable physical area.
- A plot MUST NOT have more than one active lease at the same time.
- A plot MUST NOT have more than one active crop cycle at the same time.
- A lease MUST define start, expected end, status, assigned player, plot, service package, and harvest policy.
- A player MUST only access detailed media and controls for plots assigned to that player.
- Lease activation MUST fail when the plot is unavailable, under maintenance, unsafe, or already assigned.

## Crop selection

- A player MAY only select crops compatible with the plot, season, service package, and farm capabilities.
- Crop selection becomes immutable after the crop cycle reaches the configured lock point.
- Changing crop after planting requires cancellation or a new crop cycle.

## Harvest ownership

- The player's harvest entitlement MUST be linked to the active lease and crop cycle.
- The player is entitled to all accepted and safe produce from the assigned crop cycle unless the service package explicitly defines another rule.
- Unsafe, contaminated, or legally non-deliverable produce MUST NOT be delivered.
- Rejected produce, losses, and quality decisions MUST be recorded.
- Compensation for platform-caused failure MUST follow an explicit policy.
- The platform MUST NOT silently substitute produce from another plot.

## Player actions

- A player action is a request.
- A player request MUST be validated by an action policy.
- The policy result MUST be one of:
  - `accepted_for_automation`;
  - `accepted_for_work_order`;
  - `scheduled`;
  - `rejected`;
  - `requires_expert_review`;
  - `expired`.
- The response MUST include a human-readable reason.
- Emergency safety automation MUST override player preferences.
- Player requests MUST NOT directly control pesticide use, destructive pruning, crop removal, or unsafe actuator duration.

## Automation

- Every actuator command MUST record source, reason, target, requested duration, actual duration, status, and timestamps.
- Repeated commands MUST be idempotent.
- A watchdog MUST stop devices that exceed safe limits.
- Failed acknowledgements MUST not be reported as completed actions.
- An operator override MUST be logged and must include a reason.

## Work orders

- Manual agricultural work MUST be represented by a work order.
- Work orders MAY combine compatible requests across plots to reduce operational cost.
- A work order MUST have priority, assignee, due window, status, and affected plots.
- Completion SHOULD include before/after evidence.
- Missing evidence requires an explicit reason and reviewer approval.
- A player sees customer-safe status and evidence, not internal staff notes that contain sensitive information.

## Incidents and replacement

- Crop failure MUST create an incident record.
- A replacement plot or crop MUST require customer notification.
- Historical records MUST remain accessible after replacement.
- A replacement MUST create a new assignment link rather than mutating old history.
- Compensation status MUST be traceable.

## Camera and privacy

- Camera access MUST be limited to authorized plots and permitted time windows.
- The system SHOULD prefer plot-focused snapshots for MVP.
- Personal information of workers SHOULD not be exposed in customer media.
- Camera downtime MUST show the last valid image and an offline state.

## Treatments and food safety

- Chemical treatment MUST be entered by an authorized operator.
- Treatment records MUST include product, active ingredient when applicable, dosage, operator, timestamp, and withdrawal period.
- Harvest MUST be blocked or warned when the withdrawal period is not satisfied.
