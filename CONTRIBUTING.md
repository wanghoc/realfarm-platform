# Contributing

## Branch strategy

`main` is protected and should remain demonstrable. Use short-lived feature branches.

Examples:

```text
feat/42-plot-lease
fix/57-watering-policy
docs/18-update-domain-rules
```

Avoid a long-lived `develop` branch unless the team explicitly adopts one later.

## Commit format

Use Conventional Commits:

```text
<type>(optional-scope): <imperative summary>
```

Allowed common types:

- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`
- `build`
- `ci`

Examples:

```text
feat(leases): activate a plot lease
fix(automation): cap watering duration
test(work-orders): cover rejected completion
docs(scope): move blockchain out of MVP
```

## Pull request rules

A pull request should:

- reference the task or issue;
- explain the user-visible behavior;
- list important technical decisions;
- include tests;
- include screenshots for UI changes;
- note migrations and environment changes;
- stay focused;
- pass all configured checks;
- receive at least one review.

Aim for a reviewable size. When a PR becomes large, split it by vertical behavior instead of technical layers.

## Review priorities

Review in this order:

1. safety and business-rule correctness;
2. authorization and data isolation;
3. state transitions and failure recovery;
4. tests;
5. maintainability;
6. style.

## Merge policy

Use squash merge unless preserving commit history has a clear benefit. The final commit message must follow Conventional Commits.

## Secrets and generated assets

Never commit:

- `.env`;
- credentials and private keys;
- Fabric crypto material;
- raw datasets;
- trained model binaries;
- camera recordings;
- production database dumps;
- user personal data.

Use `.env.example` and documented setup scripts.
