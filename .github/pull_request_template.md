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

The description may be written in Vietnamese — it is what the team reads to review. The
PR title and commit messages stay in English (AGENTS.md §5). Keep identifiers, field
names, enum values, error codes, and file paths in English everywhere, so they stay
greppable.
-->

## Summary

Describe the user-visible or system behavior.

## Related task

Closes #

## Changes

- 

## Business rules affected

- 

## How to Test

<!--
Keep this section when the change adds or alters behavior someone can exercise. Delete
it for docs-only or config-only PRs, which have nothing to run.

Number the steps so a reviewer can follow them without guessing, and include at least
one failure case — a happy path on its own hides the bugs worth finding. This repository
keeps no committed automated test tree (docs/09_VALIDATION_STRATEGY.md), so these steps
are how a reviewer verifies the change for themselves.
-->

1. 

## Validation

<!--
List the checks this change actually needed and what they showed. Derive them from what
you changed rather than ticking a fixed list — a checklist copied from the template
tells a reviewer nothing they can trust.

docs/09_VALIDATION_STRATEGY.md lists the code-level checks available: ruff lint/format,
app import check, type-check, lint, build, simulator import and scenario run.
-->

- [ ] 

Always keep these two, even to record that they do not apply:

- [ ] Authorization checked
- [ ] Failure behavior checked

## Screenshots or evidence

Add when applicable.

## Migrations / environment changes

None / describe.

## Risks and follow-up

- 
