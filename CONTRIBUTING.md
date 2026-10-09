# Contributing to Kiomon

Thanks for taking the time to contribute. This guide applies to every repository in the
[`kiomon-hq`](https://github.com/kiomon-hq) organisation.

## Before you start

- **Bug reports and feature requests** — open an issue in the repository you are working in. The
  issue templates ask for the detail that makes a report actionable.
- **Security vulnerabilities** — do **not** open a public issue. Follow the
  [security policy](SECURITY.md).
- **Large changes** — open an issue describing the change before writing the code. It is the
  cheapest way to find out whether the change fits the SDK's design, which for the SDKs is
  deliberately conservative: the public surface mirrors the service and the agent-facing tools,
  so it cannot drift freely.

## Making a change

1. Fork the repository and branch from `main`.
2. Make the change, with tests. A behaviour change without a test will be asked for one.
3. Run the repository's checks locally — every repository documents them in its README, and
   they are the same commands CI runs.
4. Open a pull request against `main` with a short description of the problem and the approach.
   Link the issue it closes, if there is one.
5. `main` is protected: CI must be green and the pull request reviewed before it merges.

Keep commits focused and the history readable. Rebase rather than merge `main` into your branch.

## Conventions

**Everything is in English.** Code, comments, commit messages, issues and pull requests.

**The wire contract is shared.** The Python and TypeScript SDKs, and the MCP tools, describe the
same requests and responses. Method names are the tool names; field names are the wire names.
A change to one surface that is not mirrored in the others is a bug, not a stylistic choice — say
so in the pull request if you believe a divergence is warranted.

**Comments explain why, not what.** The code says what it does. A comment earns its place by
recording the reason: the constraint that forced the shape, the tempting alternative that was
wrong, the failure it prevents.

**No new runtime dependencies** in the SDKs unless there is no reasonable alternative. Both SDKs
use only their language's standard library, and that is a feature — say so in the pull request if
you think a dependency is justified.

### Style

| Language | Formatting | Linting | Types | Tests |
|---|---|---|---|---|
| Python | ruff (`ruff check`) | ruff | mypy (strict) | pytest |
| TypeScript | 2-space indent, tabs are not used | `tsc` | `tsc --noEmit` (strict) | vitest |

Repository-specific settings live in `pyproject.toml` and `tsconfig.json`; do not reformat
unrelated code in a pull request.

## Commit messages

A short imperative subject line, then a blank line and a body explaining the change and why it is
needed. Reference the issue where relevant.

```
Reject an empty query before the request is sent

validate_client_options accepted "" and the server answered with a
validation_failed the caller could not tell apart from a transport
problem. An empty query is a programming error, so it now raises
synchronously like the other argument checks.
```

## Licensing

By contributing you agree that your contribution is licensed under the repository's licence
(MIT). There is no separate contributor licence agreement and no copyright assignment.
