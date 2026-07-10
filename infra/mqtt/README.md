# MQTT

## Topic convention

Proposed topics:

```text
realfarm/v1/gateways/{gatewayId}/telemetry
realfarm/v1/gateways/{gatewayId}/commands
realfarm/v1/gateways/{gatewayId}/acknowledgements
realfarm/v1/gateways/{gatewayId}/status
```

Use authenticated clients outside local development. Payloads must follow versioned shared contracts.
