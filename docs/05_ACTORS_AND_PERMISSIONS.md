# Actors and Permissions

## Player

Can:

- manage own profile;
- browse available plots;
- request or activate a lease;
- select allowed crops;
- view own digital farm;
- view own telemetry summary and media;
- submit allowed action requests;
- view customer-safe work-order progress;
- view care history and harvest entitlement;
- request pickup or delivery.

Cannot:

- directly bypass safety policies;
- control chemical treatment;
- access other players' plots;
- edit historical farm records;
- mark work orders complete.

## Farm Operator

Can:

- view assigned work orders;
- accept, start, block, and complete work;
- upload evidence;
- create care logs;
- record incidents;
- record harvest measurements;
- perform authorized overrides with reasons.

Cannot:

- change commercial lease terms;
- access unrelated customer data beyond operational need;
- delete audit history.

## Agronomy Expert

Optional role for MVP but useful in the model.

Can:

- review risky player requests;
- define crop rules and thresholds;
- approve treatments;
- review disease predictions;
- approve exceptional crop actions.

## Administrator

Can:

- manage users, farms, plots, devices, crop catalog, and service packages;
- approve leases;
- assign work;
- resolve incidents and compensation;
- view system audit data;
- manage integration settings.

## System Automation

Can:

- ingest telemetry;
- evaluate policies;
- create commands;
- create alerts;
- create work-order drafts;
- enforce watchdog and emergency actions.

The system actor cannot erase human accountability; every automated decision must record inputs and rule version.
