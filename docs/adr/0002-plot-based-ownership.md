# ADR 0002 — Lease Real Plots, Not Individual Plants

- Status: Accepted

## Context

Sensors, irrigation, cameras, labor, and harvesting naturally operate by area or batch. Individual-plant ownership creates operational ambiguity and high labor cost.

## Decision

The customer leases a defined real plot or micro-plot for one crop cycle. The resulting accepted harvest belongs to that customer's entitlement.

## Consequences

- Easier sensor and camera mapping.
- Clearer harvest segregation.
- Better alignment with work-order batching.
- UI may display individual plant sprites, but ownership is defined at plot/crop-cycle level.
