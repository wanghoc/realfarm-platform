<!--
Delete every section below that does not apply to this change, rather than keeping it
and writing "N/A". A backend-only change carries no frontend or UI section; a change
with no migration carries no migration section. The PR should show what changed, not
enumerate what did not.

Two exceptions, under Validation — keep them even when the answer is "does not apply":

  - Authorization checked
  - Failure behavior checked

AGENTS.md §2 treats these as invariants. If they are simply absent, a reviewer cannot
tell "not applicable" apart from "nobody looked".

Always keep: Summary, Related task, Changes, Validation.
-->

## Summary

Describe the user-visible or system behavior.

## Related task

Closes #

## Changes

- 

## Business rules affected

- 

## Validation

Keep the lines that apply; delete the rest. See `docs/09_VALIDATION_STRATEGY.md`.

- [ ] Backend validation
- [ ] Frontend validation
- [ ] API/contract validation
- [ ] Manual UI verification

Always keep these two, even to record that they do not apply:

- [ ] Authorization checked
- [ ] Failure behavior checked

## Screenshots or evidence

Add when applicable.

## Migrations / environment changes

None / describe.

## Risks and follow-up

- 
