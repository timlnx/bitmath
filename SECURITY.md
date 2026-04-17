# Security Policy

Generally speaking, users will be encouraged to update to newer versions. Since the launch of this project in 2014 I have been committed to introducing non-breaking changes and strong forward/backward compatibility. The 2.0.0 release series is the first time in over a decade that breaking changes have been introduced. Most likely, the response will always be "update to the latest 2.x" for the latest patches.

Security related bugs should be reserved for situations with actual real-life consequences. Inappropriate use of the library, "user-error", generally won't fall under this umbrella.

## Supported Versions

As of the 2.0.0 re-factor only versions ≥ 2.0.0 will receive support. Versions prior to 2.0.0 are legacy and not recommended for general use. The last "update" to the pre 2.0.0 series was 1.4.0 in April of 2026, nearly 8 years after the 1.3.3 release made in 2018.

| Version | Supported          |
| ------- | ------------------ |
| `≥ 2.0.0`   | :white_check_mark: |
| `< 2.x.y`   | :x:              |

This list will be updated when future releases are made in the 2-version series that require specific callouts for supportability.

## Reporting a Vulnerability

If you have discovered what you think is a harmful bug with the potential for exploitation that will lead to loss of life or data, then reach out to the maintainer at this email address:

* `bitmath@lnx.cx`

Please include a tag in the subject indicating the sensitivity of the issue. I will respond and we will triage the issue, a disclosure statement will be made as soon as we understand the potential impact and have prepared a mitigation.

As an emergency backup you can find me on bsky or instagram and direct message me there:

* [bsky - @lnx.cx](https://bsky.app/profile/lnx.cx)
* [insta - @tim.lnx](https://www.instagram.com/tim.lnx/)

For less serious security issues with lower potential for exploitation or damage, please open a bug on the project and apply the `security` label to it.

