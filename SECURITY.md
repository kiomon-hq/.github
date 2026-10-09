# Security Policy

## Reporting a vulnerability

**Please do not report security vulnerabilities through public issues, pull requests or
discussions.**

Report privately through GitHub's private vulnerability reporting on the affected repository:
open the **Security** tab and choose **Report a vulnerability**. This opens a private advisory
visible only to you and the maintainers, and lets us credit you in the published advisory if you
would like.

If you cannot use that form, email **security@kiomon.com**.

Please include, as far as you can:

- the repository, package and version affected;
- what an attacker can do, and what access they need to do it;
- reproduction steps or a proof of concept;
- any suggested fix or mitigation.

## What to expect

| Stage | Target |
|---|---|
| Acknowledgement of your report | within 3 business days |
| Initial assessment and severity | within 7 business days |
| Fix or mitigation for a confirmed high-severity issue | as fast as the fix can be shipped safely |
| Public advisory | published when a fixed version is available, coordinated with you |

We will keep you informed of progress, and we will credit you in the advisory unless you prefer
otherwise. Please give us a reasonable window to release a fix before any public disclosure.

## Supported versions

The SDKs are pre-1.0 and are released from `main`. Security fixes are issued as a patch release of
the latest published version; older versions are not maintained.

## Scope

In scope: the SDK source in the repositories in this organisation, and the packages published from
them to PyPI and npm.

Out of scope: vulnerabilities in the hosted Kiomon service itself — report those to
**security@kiomon.com** instead — and issues that require a compromised developer machine, a
malicious dependency you install yourself, or a browser or runtime that is already unsupported.

## Safe harbour

We will not pursue legal action against researchers who act in good faith under this policy:
testing only against their own accounts and data, not accessing or modifying other users' data,
not degrading the service, and reporting findings to us before disclosing them publicly.
