# Gateway

The gateway connects MQTT, sensors, actuators, and camera/media capture.

## Responsibilities

- read device data;
- normalize units;
- attach timestamp and device identity;
- publish telemetry;
- receive validated commands;
- enforce local safety limits;
- acknowledge commands;
- report final device state;
- buffer temporarily during network loss.

The gateway contract must match the simulator contract.
