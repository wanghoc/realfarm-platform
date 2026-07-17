# Assumptions and Open Questions

These items must be reviewed before implementation becomes irreversible.

## Commercial model

- What is the plot size?
- Is the lease priced per crop cycle, month, or service package? *(Note: The `ServicePackage` and `HarvestPolicy` enums with values like `BASIC`/`FULL_SERVICE`/`PREMIUM` and `ALL_TO_PLAYER`/`SHARED`/`MARKET_SELL` have been temporarily defined to support the MVP models, but this remains an open question pending a final business decision.)*
- How many manual requests are included?
- Are extra requests chargeable?
- Is a minimum yield guaranteed?
- What compensation applies to crop failure?

## Agriculture

- Which tomato variety is the MVP crop?
- Which growing method is used: soil, substrate, hydroponic, or another method?
- Which actions may players request?
- Which actions require expert approval?
- Are pesticides allowed in the project demonstration?
- What are the validated thresholds and their source?

## Operations

- What is the operator service window?
- What is the SLA for manual requests?
- How are tasks batched?
- How is produce physically separated by plot?
- How is pickup or delivery handled?

## Technology

- Is real payment integration required for defense?
- Are pH and light sensors available?
- Is Raspberry Pi required, or can another gateway be used?
- Is live streaming required, or are snapshots enough?
- Is Hyperledger Fabric explicitly required by the supervisor?

## Legal and communication

- What disclaimer explains biological risk?
- What personal data is collected?
- How long is camera media retained?
- What public traceability information may be shown?
