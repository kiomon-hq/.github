# Kiomon organisation defaults

This repository holds the [`kiomon-hq`](https://github.com/kiomon-hq) organisation's community
health files and its public profile. It contains no product code — the only code here is the script
that draws the profile banner.

## What lives here

| Path | Effect |
|---|---|
| `profile/README.md` | The page shown at [github.com/kiomon-hq](https://github.com/kiomon-hq) |
| `profile/assets/` | The banner and mark that page uses — generated, never drawn by hand |
| `tools/build-banner.py` | Regenerates `profile/assets/`; fonts and provenance in `tools/fonts/` |
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

## What is public, and what is not

Three repositories are public: `python-sdk`, `typescript-sdk` and `docs`. Both SDKs are MIT. The docs
repository is published to be read and is not open source, and everything else — the service, the
engine, the apps, this organisation's own infrastructure — is closed.

Keep that in mind here, because these files are org-wide defaults: anything written for one
repository lands in all of them. In particular, do not describe the **product** as open source. The
SDK clients are open source; Kiomon is not. "Public" is the safe word where you mean "you can read
it on GitHub".

## The profile banner

`profile/assets/banner-light.svg` and `banner-dark.svg` are the same plate in the two themes GitHub
renders, selected by the `<picture>` element at the top of `profile/README.md`. `logo-mark.svg` is
the mark on its own, for anything that needs it without the wordmark.

They are generated, not exported:

```sh
pip install fonttools uharfbuzz
python tools/build-banner.py --preview out   # --preview also writes PNGs, needs Chrome
```

The lockup is the landing page's own — the mark, Bricolage Grotesque SemiBold for the wordmark,
Inter for the supporting line, the hero's halftone field — and the wordmark is **outlined rather
than set as `<text>`**, because GitHub serves README images through a proxy that has never seen the
site's webfonts; a `font-family` there resolves to Arial. Optical size is applied per string from
the variable axes in `tools/fonts/`, which is what keeps a display-size wordmark the same cut as
the hero headline instead of the text face.

The README references the SVGs by absolute `raw.githubusercontent.com` URL. Relative paths do not
resolve reliably in an organisation profile README, and a rename is one `grep` — the two URLs are
the only places the organisation name appears in that file.

## Changing something here

Open a pull request. Because these are org-wide defaults, a change here needs a maintainer review
before it merges. Keep the prose concrete: these files are read by people deciding whether to
trust the project, and by people reporting a bug at their most frustrated.

## Contact

- Security: private vulnerability reporting, per [`SECURITY.md`](SECURITY.md)
- Conduct: **conduct@kiomon.com**
- Everything else: an issue in the repository concerned
