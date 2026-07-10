# ADR 0001 — Use a Modular Monolith for the Core Backend

- Status: Accepted

## Context

The team has four members, a sixteen-week schedule, and evolving domain rules. A full microservice architecture adds deployment, observability, transaction, and integration overhead.

## Decision

Build the transactional backend as one FastAPI deployable with strict internal modules. Keep AI runtime separate.

## Consequences

- Faster local setup and debugging.
- Easier transactional consistency.
- Module boundaries must be enforced by code structure and review.
- Future extraction remains possible when a measured need appears.
