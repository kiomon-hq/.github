# Kiomon organisation defaults

This repository holds the [`kiomonai`](https://github.com/kiomonai) organisation's community
health files and its public profile. It contains no product code.

## What lives here

| Path | Effect |
|---|---|
| `profile/README.md` | The page shown at [github.com/kiomonai](https://github.com/kiomonai) |
| `CONTRIBUTING.md` | Default contributing guide for every repository that does not define its own |
| `CODE_OF_CONDUCT.md` | Default code of conduct — Contributor Covenant 2.1 |
| `SECURITY.md` | Default security policy; points at private vulnerability reporting |
| `SUPPORT.md` | Default support and "where to ask" guide |
| `ISSUE_TEMPLATE/` | Default issue forms used by repositories without their own |
| `PULL_REQUEST_TEMPLATE.md` | Default pull request template |

GitHub applies these automatically to every repository in the organisation that does not define
the same file itself, so the SDK repositories do not carry duplicates. Editing a file here changes
it for every repository at once — including already-published content — so prefer a repository-level
file when a repository genuinely needs to differ.

## Changing something here

Open a pull request. Because these are org-wide defaults, a change here needs a maintainer review
before it merges. Keep the prose concrete: these files are read by people deciding whether to
trust the project, and by people reporting a bug at their most frustrated.

## Contact

- Security: private vulnerability reporting, per [`SECURITY.md`](SECURITY.md)
- Conduct: **conduct@kiomon.com**
- Everything else: an issue in the repository concerned
