# Changes from the Original Proposal

## Summary

The original proposal focused on smart-greenhouse management for farmers, with consumers mainly scanning QR codes after harvest. The revised project is a customer-facing remote-farming service where a player leases a real plot, chooses a crop, participates through a game-like interface, and owns the resulting harvest.

## Change matrix

| Area | Original direction | Revised direction |
|---|---|---|
| Primary product | Smart greenhouse management | Remote farming experience platform |
| Primary user | Farmer | Player/customer |
| Consumer role | QR traceability reader | Plot lessee and harvest owner |
| Farm worker | Implicit inside farmer actor | Explicit operator actor with work orders |
| Digital Twin | Monitoring dashboard with game style | Main player interaction surface |
| Player control | Manual override had highest priority | Player sends policy-controlled requests |
| Safety priority | Farmer manual override | Emergency automation and authorized operator override |
| Core transaction | Crop monitoring and traceability | Plot lease → crop cycle → action execution → harvest entitlement |
| Manual care | Care log entered by farmer | Work-order system with scheduling and evidence |
| Commerce | Cost accounting for farmer | Service package, lease terms, entitlement, pickup/delivery |
| Harvest | Farm records yield | Produce belongs to the assigned player under policy |
| Replacement | Buffer plot suggested | Transparent incident and replacement workflow |
| Architecture | Broad microservice direction | Modular monolith plus separate AI service |
| Mobile | Flutter/mobile suggested early | Responsive web/PWA first |
| Camera | Realtime stream per plot | Snapshot or limited on-demand stream for MVP |
| Sensors | Five sensors as baseline | Three essential sensors first; pH/light optional |
| AI | Multiple AI functions | One validated MVP feature at most |
| Blockchain | MVP-heavy Hyperledger Fabric | Optional extension behind adapter |
| Timeline | Long analysis phase, late coding | Early vertical-slice implementation |
| Success measure | Many technologies integrated | Safe end-to-end real-world interaction |

## Features retained

- real plot and crop-cycle management;
- IoT telemetry;
- automated irrigation;
- watchdog safety;
- Digital Twin;
- camera/media;
- care history;
- disease detection as a candidate AI feature;
- traceability and QR;
- hardware simulator.

## New required modules

- plot leasing;
- service packages;
- crop compatibility;
- player action requests;
- action policy engine;
- work orders and operator portal;
- work evidence;
- incidents and replacement;
- harvest entitlement;
- pickup/delivery;
- customer notifications.

## Reduced or postponed modules

- advanced yield estimation;
- automatic produce grading;
- multi-crop support;
- complex cost analytics;
- multi-organization blockchain;
- native mobile application.
