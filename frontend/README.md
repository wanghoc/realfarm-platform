# Web/PWA Application

React + TypeScript web application with a feature-first structure.

## Feature areas

- authentication;
- player dashboard;
- plot browsing and status;
- lease onboarding;
- crop selection;
- farm visualization;
- action request panel;
- timeline and media;
- notifications;
- harvest and delivery;
- operator portal;
- admin portal.

## Current structure

```text
src/
  features/
    auth/
    dashboard/
    farm/
    operator/
    plots/
  shared/
    api/
    components/
    layouts/
    pages/
    store/
```

## Boundary rule

The frontend must never treat UI state as the source of truth for real-world actions. Any future game-rendering adapter must sit behind API state and must show accepted, scheduled, rejected, expired, and completed states honestly.
