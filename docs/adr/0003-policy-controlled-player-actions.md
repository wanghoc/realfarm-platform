# ADR 0003 — Player Actions Are Policy-Controlled Requests

- Status: Accepted

## Context

A game interface may suggest direct control, but unrestricted real-world actions can harm crops, devices, food safety, and operations.

## Decision

Every player action becomes a request evaluated by an action policy. It may produce an automation command, a work order, a schedule, expert review, or rejection.

## Consequences

- The UI must represent pending and rejected states.
- Policy versions and reasons must be recorded.
- Emergency automation and authorized operators retain override capability.
