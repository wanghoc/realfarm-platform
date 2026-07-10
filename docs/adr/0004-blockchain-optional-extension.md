# ADR 0004 — Keep Blockchain Outside the MVP Core

- Status: Accepted

## Context

Hyperledger Fabric is technically expensive and does not prove that source data was truthful. The product can demonstrate traceability with off-chain records, audit logs, media evidence, and hashes.

## Decision

Create a traceability adapter. The default implementation stores hashes off-chain. A Fabric adapter may be added after the core vertical slice is stable or when the supervisor explicitly requires it.

## Consequences

- Core operations continue during blockchain failure.
- No raw data is written on-chain.
- Blockchain work cannot delay lease, action, work-order, or harvest flows.
