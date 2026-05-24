# Security Policies

This document defines bitmath's policies for handling findings from
Software Composition Analysis (SCA), Static Application Security
Testing (SAST), and license compliance scanning. It exists so
downstream consumers can understand the project's commitments and so
future maintainers can apply the policies consistently.

The threat model that motivates these policies is in
[SECURITY_ASSESSMENT.md](SECURITY_ASSESSMENT.md). The vulnerability
reporting process is in [SECURITY.md](SECURITY.md). The release
verification process is in [VERIFICATION.md](VERIFICATION.md). The
workflows that enforce these policies live in `.github/workflows/`.

## Software Composition Analysis (SCA)

SCA covers known vulnerabilities and license compliance in
bitmath's dependencies. Because bitmath has **zero runtime
dependencies** (verifiable in `pyproject.toml`), the operational
scope of SCA is the development dependency set listed in
`requirements.txt`.

### Tools

* **Dependabot** opens pull requests for dependency updates and
  surfaces known vulnerabilities. Configured in
  `.github/dependabot.yml`.
* **pip-audit** runs on every push and pull request via
  `.github/workflows/sca.yml` against `requirements.txt`. The
  workflow is a required status check on `master`.
* **GitHub secret scanning** (enabled at the repository level)
  catches credentials accidentally committed to the repository.

### Remediation Thresholds

Severity ratings follow the CVSS score reported by the SCA tool.
The remediation clock starts when the finding becomes visible in
the project (Dependabot alert or `pip-audit` CI failure).

| Severity | CVSS range | Action | Timeline |
|----------|-----------|--------|----------|
| Critical | 9.0 – 10.0 | Patch or replace the affected dependency. Block any release until remediated. | Within 7 days of disclosure |
| High | 7.0 – 8.9 | Patch or replace the affected dependency. Block release if the next release is within 30 days; otherwise remediate before that release. | Within 30 days of disclosure |
| Medium | 4.0 – 6.9 | Patch when the next dependency update naturally cycles through. | Within 90 days |
| Low | 0.1 – 3.9 | Patch opportunistically. | Best effort |

A finding may be suppressed only when it is demonstrably
non-exploitable in bitmath's usage of the dependency. Suppression is
documented inline in the SCA workflow configuration with a comment
explaining why.

### Release Blocking

A release of bitmath **MUST NOT** ship while a Critical or High SCA
finding against a dev dependency is unaddressed, unless the finding
has been formally suppressed as non-exploitable per the rule above.
The `.github/workflows/sca.yml` status check enforces this on the
merge path; the release process (see
[ARCHITECTURE.md](ARCHITECTURE.md)) is gated by the same branch
protection.

### License Compliance

All direct dependencies must use a license listed as
[OSI-approved](https://opensource.org/licenses) or
[FSF-approved](https://www.gnu.org/licenses/license-list.html).
Today every dev dependency uses MIT, Apache 2.0, or BSD. Adding a
new dev dependency that introduces a copyleft license (GPL, AGPL,
LGPL) requires explicit consideration before being merged; the PR
that introduces it must document the decision in the description.

## Static Application Security Testing (SAST)

SAST covers security weaknesses in bitmath's own source code.

### Tools

* **Bandit** scans `bitmath/` and `tests/` for common Python
  security smells. Runs on every push and pull request via
  `.github/workflows/bandit.yml`. Required status check.
* **CodeQL** performs semantic analysis for Python vulnerabilities.
  Runs on every push, pull request, and weekly via
  `.github/workflows/codeql.yml`. Required status check.
* **OSSF Scorecard** performs a weekly meta-analysis of repository
  security posture. Reports to the GitHub Security tab.

### Remediation Thresholds

| Severity | Action | Timeline |
|----------|--------|----------|
| High | Fix in the next patch release. Block any merge that introduces a new High finding. | Within 7 days for existing findings; immediately for new ones |
| Medium | Fix in the next minor release. | Within 30 days |
| Low | Address in the normal development cycle. | Best effort |
| Informational | Triage and either fix or suppress with a justifying comment. | Best effort |

A finding may be suppressed only when it is a true false positive.
The suppression must include a `# nosec` comment with an inline
justification (Bandit) or a `# lgtm[py/...]` annotation (CodeQL)
explaining the rationale. The justification should be specific
enough that a future maintainer can re-evaluate the suppression
without re-deriving the analysis.

### Release Blocking

A release of bitmath **MUST NOT** ship while any High SAST finding
against the project's own code is unaddressed, unless the finding is
formally suppressed as a false positive per the rule above. The
Bandit and CodeQL required status checks enforce this on the merge
path.

## Review and Updates

This policy is reviewed at every minor release. The contract:

* A new SAST or SCA tool added to CI → update the corresponding
  Tools section.
* A change to remediation thresholds or release-blocking rules →
  update the corresponding table and re-state the rationale in the
  commit message.
* A suppression added in code → also add a brief justification in
  the suppression comment so the rationale survives the next
  review.

If this policy drifts out of sync with what the workflows actually
enforce, that is a defect worth [opening an
issue](https://github.com/timlnx/bitmath/issues/new) or a PR.
