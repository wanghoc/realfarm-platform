# Database

Use PostgreSQL with TimescaleDB enabled for telemetry.

Rules:

- schema changes through migrations;
- seed only non-sensitive development data;
- no production dumps in Git;
- use explicit constraints for active lease/crop-cycle invariants;
- use durable job tables for retryable asynchronous work.
