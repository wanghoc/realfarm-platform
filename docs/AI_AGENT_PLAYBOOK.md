# AI Agent Playbook

## Before coding

Use this checklist:

```text
[ ] I read AGENTS.md.
[ ] I read scope and business rules.
[ ] I identified the affected aggregate and state transition.
[ ] I checked related contracts and ADRs.
[ ] I know the authorization rule.
[ ] I know the failure behavior.
[ ] I know which validation steps prove the change.
```

## Preferred task response

An agent working in the repository should provide:

1. **Understanding**
2. **Plan**
3. **Files to change**
4. **Implementation**
5. **Validation**
6. **Risks/assumptions**

## Avoid

- creating parallel services for every noun;
- placing business logic in controllers;
- optimistic UI that reports real-world completion too early;
- hidden fallback that swaps a player's produce;
- treating AI output as unquestionable truth;
- adding blockchain to unrelated workflows;
- changing contracts without versioning or coordination.

## Context refresh triggers

Re-read core docs when:

- a task changes harvest ownership;
- a task changes player permissions;
- a task adds an actuator action;
- a task changes lease or crop-cycle state;
- a task introduces new infrastructure;
- a task changes data exposed through QR;
- a task changes incident or compensation behavior.
