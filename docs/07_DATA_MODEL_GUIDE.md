# Data Model Guide

This document is a conceptual guide. The final SQL schema must be created through migrations.

## Core tables

- `users`
- `roles`
- `farms`
- `greenhouses`
- `plots`
- `crop_catalog`
- `service_packages`
- `leases`
- `plot_assignments`
- `crop_cycles`
- `devices`
- `sensors`
- `actuators`
- `measurements`
- `action_policies`
- `player_action_requests`
- `automation_commands`
- `work_orders`
- `work_order_items`
- `work_evidence`
- `care_logs`
- `ai_inferences`
- `incidents`
- `replacement_assignments`
- `harvest_batches`
- `harvest_entitlements`
- `delivery_orders`
- `notifications`
- `traceability_records`
- `audit_logs`
- `durable_jobs`

## Important constraints

- Unique active lease per plot.
- Unique active crop cycle per plot.
- Player-action request belongs to the player, lease, plot, and crop cycle.
- Work-order item belongs to exactly one plot and crop cycle.
- Harvest entitlement cannot exceed accepted harvest quantity.
- Measurement unit must match sensor type.
- Completed commands require an acknowledgement or a reviewed manual resolution.
- Historical care and harvest records are append-oriented.

## Public identifiers

Use opaque public identifiers. Do not expose predictable internal sequence IDs when authorization mistakes could reveal neighboring records.

## Time

Store timestamps in UTC. Keep the farm timezone in farm settings for display and scheduling.

## Audit

High-risk tables should record actor, source, reason, created time, updated time, and version where appropriate.
