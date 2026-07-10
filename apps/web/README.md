# Web/PWA Application

React + TypeScript with Phaser 3 embedded for the 2D farm.

## Feature areas

- authentication;
- plot marketplace/listing;
- lease onboarding;
- crop selection;
- player dashboard;
- Phaser farm scene;
- action request panel;
- timeline and media;
- notifications;
- harvest and delivery;
- operator portal;
- admin portal.

## Phaser boundary

Phaser renders the experience. It must not own transactional truth.

Use an adapter:

```text
API state
→ view model
→ Phaser scene
→ user intent event
→ application command
```

The game scene must show pending, scheduled, failed, and completed states honestly.
