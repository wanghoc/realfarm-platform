# Testing Strategy

## Test pyramid

### Domain unit tests

Test:

- lease activation;
- crop compatibility;
- one-active-lease invariant;
- player action policy decisions;
- work-order transitions;
- harvest entitlement calculations;
- replacement transparency;
- withdrawal-period checks.

### Integration tests

Test:

- repositories and migrations;
- transaction boundaries;
- telemetry ingestion;
- durable job retry;
- MQTT publish/acknowledgement flow;
- media metadata persistence;
- optional blockchain adapter failure behavior.

### API contract tests

Test:

- authentication and authorization;
- ownership isolation;
- validation errors;
- state-transition conflicts;
- idempotency;
- pagination and filtering.

### End-to-end tests

Minimum critical scenarios:

1. lease plot and start crop cycle;
2. player request accepted for automation;
3. player request converted to work order;
4. unsafe request rejected;
5. operator completes work with evidence;
6. crop incident and replacement;
7. harvest creates player entitlement.

## Hardware testing

The same contract suite must run against:

- simulator;
- gateway test environment;
- selected real hardware.

## AI testing

Record:

- dataset version;
- train/validation/test split;
- baseline;
- metrics;
- confidence threshold;
- known failure cases;
- inference latency.

## Definition of done

A feature is done when:

- acceptance behavior is implemented;
- required tests pass;
- authorization is verified;
- failure behavior is handled;
- contracts are updated;
- documentation reflects changed rules;
- no known safety invariant is bypassed.
