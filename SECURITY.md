# Security Policy

## Sensitive areas

This project handles:

- user accounts and lease data;
- farm camera images;
- device identities and commands;
- agricultural treatment records;
- delivery information;
- optional payment references.

## Mandatory controls

- JWT-based authentication with role and ownership checks.
- TLS for HTTP, WebSocket, and MQTT outside local development.
- Device identity validation.
- Audit logging for commands, work-order changes, treatment records, harvest records, and admin actions.
- Least-privilege access to farm, plot, and media data.
- Secret injection through environment variables or a secret manager.
- Rate limits for authentication, camera access, and player action requests.
- Signed or integrity-protected evidence metadata where practical.

## Reporting

Security issues should be reported privately to the project lead. Do not open public issues containing credentials, personal data, or exploitable details.
