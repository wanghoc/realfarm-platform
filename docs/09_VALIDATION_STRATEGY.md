# Validation Strategy

This repository does not keep a dedicated committed automated test tree.

## Code-level checks

### Backend

- Ruff lint.
- Ruff format check.
- Application import and startup check.

### Frontend

- TypeScript type check.
- ESLint.
- Production build.

### Simulator

- Import check.
- Scenario run when the change touches telemetry or command flows.

## Manual smoke checks

Use manual smoke checks for the flows that matter most:

1. log in with a demo account;
2. browse plots;
3. open the farm and dashboard views;
4. submit a player action request;
5. confirm the response state is accepted, scheduled, rejected, expired, or completed;
6. confirm the simulator still publishes telemetry;
7. confirm the API docs remain reachable.

The development demo account is `demo@realfarm.dev` with password `demo1234`.

## Definition of done

A change is ready when:

- the relevant code-level checks pass;
- the user-visible flow is exercised manually if needed;
- documentation reflects the new behavior;
- no safety invariant is bypassed.
