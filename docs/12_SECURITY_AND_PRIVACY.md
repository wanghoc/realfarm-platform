# Security and Privacy

## Authorization boundaries

- Players only access resources through their own active or historical leases.
- Operators access assigned farm operations.
- Admin access is audited.
- Media URLs must be authorization-aware or time-limited.
- QR traceability pages expose only approved public fields.

## Device trust

- Register device identity.
- Use signed messages or authenticated MQTT where practical.
- Reject unknown devices.
- Record measurement quality.
- Separate command topics from telemetry topics.

## Privacy

- Avoid exposing worker faces, private conversations, vehicle plates, or unrelated plots.
- Store only delivery data required for fulfillment.
- Define retention for camera media and evidence.
- Never use farm camera images to train AI without documented approval.

## Safety

- Treat actuator control as safety-sensitive.
- Use server-side duration limits.
- Require final-state acknowledgement.
- Allow emergency stop independent of player session.
- Record override reason and actor.
