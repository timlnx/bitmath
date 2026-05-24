# Security Policy

Generally speaking, users will be encouraged to update to newer versions. Since the launch of this project in 2014 I have been committed to introducing non-breaking changes and strong forward/backward compatibility. The 2.0.0 release series is the first time in over a decade that breaking changes have been introduced. Most likely, the response will always be "update to the latest 2.x" for the latest patches.

Security related bugs should be reserved for situations with actual real-life consequences. Inappropriate use of the library, "user-error", generally won't fall under this umbrella.

## Supported Versions

As of the 2.0.0 re-factor only versions ≥ 2.0.0 will receive support. Versions prior to 2.0.0 are legacy and not recommended for general use. The last "update" to the pre 2.0.0 series was 1.4.0 in April of 2026, nearly 8 years after the 1.3.3 release made in 2018.

| Version | Supported          |
| ------- | ------------------ |
| `≥ 2.0.0`   | :white_check_mark: |
| `< 2.x.y`   | :x:              |

### Scope of Support

* **Security fixes** are issued as patch releases on the latest minor in the 2.x series. If the current line is 2.1.x, security fixes ship as 2.1.y.
* **Bug fixes** are issued on the latest minor in the 2.x series. Older minors do not receive bug-fix backports unless the bug is also a security issue covered above.
* **Functional changes** ship in new minor releases (2.x → 2.(x+1)).

### Duration of Support

* The **2.x series** receives security fixes for as long as it is the current major. Today that is open-ended; a future 3.x release would start a deprecation clock on 2.x with at least 12 months of overlap announced in `NEWS.rst` before 2.x support ends.
* The **1.x series** (legacy) is end-of-life. No further releases will be made on 1.x. Users on 1.x should plan a migration to 2.x; the 2.x API is drop-in compatible for the documented public surface.
* The **pre-1.x series** is historical and not supported in any form.

This list will be updated when future releases are made in the 2-version series that require specific callouts for supportability.

If you have discovered what you think is a harmful bug with the potential for exploitation in a supported version series, and this bug may lead to loss of life or data, then you have two options for reporting available to you:

## [1] Self-Reporting (GitHub)

Consider using the new [Private Vulnerability Reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/privately-reporting-a-security-vulnerability) function if you want to get involved that way.

* On GitHub, navigate to the main page of the repository.
* Under the repository name, click the Security and quality tab. If you cannot see the " Security and quality" tab, select the dropdown menu, and then click Security and quality.
* Click Report a vulnerability to open the advisory form.
* Fill in the advisory details form.

...as described in the linked GitHub documentation.

## [2] Reporting a Vulnerability (Non-GitHub)

You may also reach out to me at this email address:

* `bitmath@lnx.cx`

Please include a tag in the subject indicating the sensitivity of the issue.

## Response Timeframes

I treat security reports as the top of my queue. The commitments I make to anybody who files one:

* **Acknowledgement of receipt: within 72 hours.** This is just a "got it, working on it" reply so you know the report did not get lost. If you do not hear back in three days, the email may not have made it; try one of the backup channels below.
* **Initial triage assessment: within 7 days.** This is where I tell you whether the report is reproducible, what the rough severity looks like, and what the disclosure timeline will be.
* **Coordinated disclosure: as soon as we have a fix prepared and an impact statement we both agree on.** I aim to publish a [GitHub Security Advisory](https://github.com/timlnx/bitmath/security/advisories) and a `NEWS.rst` entry alongside the patch release that contains the fix. If the issue is severe enough that disclosure has to happen before a fix is ready, we coordinate the timing together.

These are commitments, not guarantees. bitmath is maintained by one person on the side. If I am on a plane or in a hospital the clock will keep ticking and I will catch up when I land. The backup channels below exist precisely for "I tried email and got nothing back" situations.

As an emergency backup you can find me on bsky or instagram and direct message me there:

* [bsky - @lnx.cx](https://bsky.app/profile/lnx.cx)
* [insta - @tim.lnx](https://www.instagram.com/tim.lnx/)

For less serious security issues with lower potential for exploitation or damage, please open a bug on the project and apply the `security` label to it.

## Secrets and Credentials Policy

bitmath is built around the principle that **no long-lived secrets should exist in the project**. The policy is short because the implementation is austere.

### What Secrets the Project Handles

* **PyPI publish authority** is handled via [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC). The publish workflow exchanges a short-lived GitHub Actions OIDC token for upload credentials at the moment of publication. There is no long-lived PyPI API token stored as a GitHub secret.
* **Read The Docs build credentials** are managed by Read The Docs via OAuth integration with GitHub. No credentials are stored in this repo.
* **The `bitmath@lnx.cx` email address** is a forwarding alias used only for security correspondence. Compromise of that mailbox does not affect any project resource directly.

### Storage

* No secret values are stored in the repository. GitHub secret scanning is enabled at the repository level and runs continuously.
* No secret values are stored in `.github/workflows/*.yml`. The workflows authenticate via OIDC tokens, not stored credentials.
* The list of GitHub Actions secrets configured on this repository is **empty**, verifiable with `gh api /repos/timlnx/bitmath/actions/secrets`.

### Access Control

* The single maintainer (see [MAINTAINERS.md](MAINTAINERS.md)) has admin access to the repository, the PyPI project, and the Read The Docs project.
* The PyPI Trusted Publishing trust relationship is scoped to the `.github/workflows/publish.yml` workflow on `master`. Any other workflow or branch attempting to authenticate to PyPI as bitmath will be rejected.
* Two-factor authentication is required on both the GitHub account (authenticator app + GitHub Mobile, SMS disabled) and the PyPI account.

### Rotation

* OIDC tokens are short-lived (minutes) and rotated automatically on every workflow run by GitHub Actions and PyPI.
* No long-lived credentials exist, so there is no rotation schedule to maintain.
* The Trusted Publisher trust relationship itself can be revoked or re-scoped via the PyPI web UI if the workflow file ever needs to change in a way that would alter the trust boundary.

### Incident Response

If a project secret or credential is suspected to be compromised:

1. Revoke the Trusted Publisher relationship on PyPI immediately, before doing anything else. This breaks any in-flight publish attempt by an attacker.
2. Audit recent activity in GitHub Actions runs and PyPI release history for unexpected events. The PyPI publish journal and GitHub Actions logs are public and inspectable.
3. Reach out through the reporting channels above so the incident can be coordinated and disclosed.

This policy is reviewed at every minor release.
