# Shared Contracts

Versioned contracts shared by API, gateway, simulator, AI service, and web application.

Rules:

- additive compatible changes may keep the version;
- breaking changes require a new schema version;
- producers and consumers must validate payloads;
- contracts are reviewed like code;
- do not place business logic in schemas.
