# Contributor Workflow

End-to-end steps to take one issue from start to merged. This document is the shared
"how we work" runbook for the whole team.

It **complements** and does not replace:

- `CONTRIBUTING.md` — branch, commit, PR, and merge rules.
- `AGENTS.md` — mandatory rules for AI agents and developers.
- `docs/09_VALIDATION_STRATEGY.md` — what "validated" means.
- `.github/pull_request_template.md` — the PR body checklist.

Each numbered step below links to the authoritative rule so this file stays short.

## Start of day — sync your clone

Run this once at the start of each working session, before step 0. Skipping it is the
usual cause of avoidable rework: rebuilding what a teammate already merged, branching off
a stale `main`, or working from an issue checklist that has since changed.

```bash
git fetch --all --prune              # refresh remote refs, drop deleted ones
git checkout main
git log --oneline main..origin/main  # what is about to land (empty = already current)
git pull                             # fast-forward main
```

Then, before picking up work:

1. **Read what merged.** If the log above touches your module or
   `packages/contracts/schemas/*`, read the diff — a merged contract change can
   invalidate work already in progress.
2. **Rebase branches you already have open** so your PR does not drift:
   `git checkout <branch> && git rebase main`. Resolve conflicts now rather than at merge
   time. Tell the reviewer first if the branch is already under review (`AGENTS.md` §4).
3. **Re-read your issue.** Acceptance criteria and open questions get edited by
   teammates; the checklist you remember may be stale.
4. **Clear review requests waiting on you** (`gh pr status`). Unblocking a teammate's PR
   takes minutes and outranks starting new work.
5. **Prune merged local branches.** `git branch -vv` marks them `: gone]` after the
   fetch above.

## 0. Before you start — load context

1. Read in `AGENTS.md` §1 order: `docs/00`–`04`, the target module's `README.md`, and
   related ADRs in `docs/adr/`.
2. Open your issue on the board (`github.com/users/wanghoc/projects/3`). Every issue has
   an **acceptance-criteria checklist** in its body — that is your definition of done.
3. Confirm the product invariants your change must not break (`AGENTS.md` §2).

## 1. Create a branch

- Branch from an up-to-date `main`. **Never commit to or push `main`** (`AGENTS.md` §4).
- Name it `<type>/<issue>-<short-name>`, e.g. `feat/23-watering-policy`.
- Types: `feat` `fix` `docs` `refactor` `chore` `test` (`CONTRIBUTING.md`).
- CI (`.github/workflows/pr-checks.yml`) rejects branch names that break this pattern.

```bash
git checkout main && git pull
git checkout -b feat/<issue>-<short-name>
```

## 2. Implement

- Make the **smallest coherent change**; no broad refactors unless the task requires it
  (`AGENTS.md` §3).
- English for code, identifiers, API fields, comments, commits, and PR titles
  (`AGENTS.md` §5). Vietnamese is allowed only in dedicated team docs.
- Ground the change in `packages/contracts/schemas/*` and existing module code; do not
  invent new contracts without coordination.
- Week 1 / domain-lock tasks are **documentation-level** (`docs/NN_*.md`).
- Never bypass authorization or safety invariants for convenience (`AGENTS.md` §12).

## 3. Validate

Run the checks that apply (`docs/09_VALIDATION_STRATEGY.md`):

- **Backend:** `ruff check .`, `ruff format --check .`, app import check.
- **Frontend:** `npm run type-check`, `npm run lint`, `npm run build`.
- **Simulator:** import check, and a scenario run if telemetry/command flow changed.
- **Docs/contracts:** confirm no drift against the relevant JSON schema.

A change is done only when checks pass, the user-visible flow is exercised, docs reflect
the behavior, and no safety invariant is bypassed.

## 4. Commit

- Conventional Commits: `<type>(scope): <imperative summary>` (`CONTRIBUTING.md`).
- Keep each commit focused and buildable; do not mix formatting-only changes with
  behavior changes.
- Never commit `.env`, secrets, keys, datasets, model binaries, or generated media.

## 5. Open a pull request

```bash
git push -u origin <branch>
```

Open a PR into `main` using `.github/pull_request_template.md`. The PR MUST:

- reference the issue with `Closes #<issue>`;
- describe the user-visible behavior and key decisions;
- include validation notes and screenshots for UI changes;
- note migrations and environment changes;
- stay focused — one PR solves one task or one tightly related group.

The PR **title** must follow Conventional Commits; CI validates the title and branch name.

You may create the PR from the GitHub web UI or with the GitHub CLI:

```bash
gh pr create --base main --title "<conventional title>" --body-file <file>
```

## 6. Review

- Request at least one reviewer, ideally the owner of the affected area
  (see role map in `docs/KE_HOACH_16_TUAN_CHI_TIET_VI.md`).
- Reviewers check in priority order: safety & business-rule correctness → authorization
  & data isolation → state transitions & failure recovery → validation → maintainability
  → style (`CONTRIBUTING.md`).
- Address feedback with follow-up commits on the same branch.

## 7. Merge

- **Squash merge** once the PR has an approval and green CI (`CONTRIBUTING.md`).
- The final squash message must follow Conventional Commits.
- `Closes #<issue>` closes the issue automatically on merge.
- Do not force-push reviewed branches, rewrite shared history, or delete remote branches
  without explicit approval (`AGENTS.md` §4).

## 8. Track on the board

Keep the issue's board card in sync as you go:

| Stage | Board status |
|---|---|
| Not started | Todo |
| Working on the branch | In Progress |
| PR open, awaiting review | In Review |
| PR squash-merged | Done (usually automatic via `Closes #`) |

Tick each acceptance-criteria checkbox in the issue **only when it is genuinely done** —
never mark an item or the card as complete while review or validation is still pending.

## Quick reference

```text
sync (fetch + pull + rebase)  →  context (AGENTS §1)  →  branch off main
  →  implement (smallest change)  →  validate (docs/09)  →  conventional commit  →  push
  →  PR (Closes #, template)  →  ≥1 review (priority order)  →  squash merge  →  board Done
```
