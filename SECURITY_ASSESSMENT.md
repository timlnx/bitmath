# Security Assessment

This document is bitmath's standing security assessment. The goal here
is not to claim the library is bulletproof. It is to lay out, in plain
language, what the realistic threats against bitmath actually look
like, what is already in place to address them, and where the soft
spots are. Downstream consumers and packagers should be able to read
this and form their own opinion without having to reverse-engineer the
project.

I revisit this document at every minor release and whenever a new
feature introduces a new attack surface.

## What bitmath Is (and What It Isn't)

bitmath is a pure-Python library for representing and converting file
sizes between SI (decimal) and NIST (binary) unit systems. It does
arithmetic, comparisons, parsing, and formatting on size values.

The most useful framing for the threat model is what bitmath
deliberately **does not** do:

* It does **not** open network sockets, make HTTP requests, or talk to
  any external service.
* It does **not** call `eval`, `exec`, or `compile` on user input.
* It does **not** shell out to subprocesses by default. The
  `query_capacity` and `query_device_capacity` functions call into
  platform APIs (`shutil.disk_usage`, `fcntl.ioctl`, `ctypes` against
  Win32) but not via the shell.
* It has **zero runtime dependencies**. The only code that runs in a
  bitmath consumer's process is bitmath itself, the Python standard
  library, and the consumer's own application code.
* It does **not** write to disk, modify the filesystem, or maintain
  any persistent state.

This drastically narrows the realistic threat surface compared to most
Python packages on PyPI.

## Attack Surfaces

These are the places where bitmath consumes input that might originate
from a hostile source, ranked roughly by how worried I am about them.

### 1. `parse_string()` and `parse_string_unsafe()`

These take a string and return a bitmath object. If a consumer hands
bitmath an attacker-controlled string (web form input, log line,
config file from an untrusted source), the parser is in the hot path.

**What we do about it:**

* The parser is a regex-driven state machine. It does not call `eval`
  on any portion of the input.
* Unknown unit suffixes raise `ValueError`. Malformed numeric portions
  raise `ValueError`. The function will not silently coerce or accept
  nonsense.
* The hypothesis-based fuzzing tests added in 2026 (`tests/test_hypothesis.py`)
  exercise the parser with thousands of generated inputs per release
  cycle to catch crash-on-input regressions.
* The known parser quirk to be aware of: scientific-notation numbers
  do not round-trip cleanly through `parse_string` in all cases. This
  is documented and tracked, and does not constitute a security
  vulnerability (it is a precision issue, not a code-execution
  surface).

### 2. `getsize()`, `listdir()`, `query_capacity()`

These take a filesystem path and call into the operating system. If a
consumer hands bitmath an attacker-controlled path, the standard
filesystem-API risks apply ([TOCTOU](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use),
symlink races, path traversal in the *consumer's* code that
constructed the path).

**What we do about it:**

* bitmath does no path sanitization of its own. It is the consumer's
  responsibility to validate paths before passing them in. This is
  documented behavior, not negligence; sanitization rules depend on
  the consumer's threat model in ways the library cannot know.
* `listdir()` was deprecated in 2.1.0 because the API is awkward
  enough that misuse was likely. Consumers should reach for
  `os.walk()` plus `bitmath.getsize()` directly.

### 3. `query_device_capacity()`

This issues `fcntl.ioctl` calls on Linux and Win32 `DeviceIoControl`
calls on Windows against a file descriptor for a block device. Both
require elevated privileges (root on Linux, administrator on Windows)
and operate on a descriptor the consumer has already opened.

**What we do about it:**

* The Linux path uses fixed `ioctl` constants from the kernel headers
  and writes only into bytes buffers it allocated itself. The Windows
  path uses fixed control codes from the Win32 API.
* There is no string formatting into the ioctl argument and no
  untrusted-input pathway into the kernel call.
* macOS raises `NotImplementedError` because the System Integrity
  Protection model makes the call meaningless. There is no codepath
  to exploit there because there is no codepath at all.

### 4. The build and release pipeline

The build pipeline itself is an attack surface: if the publishing
workflow could be tricked into emitting a malicious wheel, every
downstream pip install would be compromised.

**What we do about it:**

* Publishing uses [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC).
  No long-lived PyPI token exists to be stolen.
* The publish workflow (`.github/workflows/publish.yml`) only fires on
  `release: published` events. It cannot be triggered by a pull
  request or a direct push.
* All GitHub Actions are SHA-pinned, not version-pinned. Action
  upgrades go through Dependabot PRs that I review individually.
* Branch protection on `master` requires all CI checks to pass, with
  `enforce_admins: true`. I cannot push a malicious commit directly
  even if my account were compromised, as long as the branch
  protection itself is not also compromised.
* Two-factor authentication is required on my GitHub account
  (authenticator app + GitHub Mobile, SMS disabled).

## Automated Security Tooling

Everything below runs on every push and pull request to `master`, plus
on a weekly schedule, and posts its findings to the GitHub Security
tab.

| Tool | What it checks | Where it lives |
|------|---------------|----------------|
| [Bandit](https://bandit.readthedocs.io/) | Common Python security smells across `bitmath/` and `tests/` | `.github/workflows/bandit.yml` |
| [CodeQL](https://codeql.github.com/) | Deeper semantic analysis for Python vulnerabilities | `.github/workflows/codeql.yml` |
| [OSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/timlnx/bitmath) | Repository security posture (token permissions, pinning, signed releases, etc.) | `.github/workflows/scorecard.yml` |
| [Dependabot](https://docs.github.com/en/code-security/dependabot) | Vulnerability alerts and security update PRs for dependencies | `.github/dependabot.yml` |
| [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning) | Prevents accidental commit of credentials | Repository setting (enabled) |

Bandit currently reports zero findings against the codebase. CodeQL
currently reports zero findings against the codebase. OSSF Scorecard
currently rates the project at 7.8/10 and climbing as the OpenSSF
Best Practices badge work lands.

## Known Vulnerabilities

None at time of writing. If any are reported and confirmed, they will
be published as [GitHub Security Advisories](https://github.com/timlnx/bitmath/security/advisories)
with the CVE number when applicable, and called out in the relevant
`NEWS.rst` section for that release.

## Reporting

See [SECURITY.md](SECURITY.md) for the reporting process, response
timeframes, and contact channels.

## Last Review

This assessment was last reviewed against the bitmath 2.1.0 working
tree.
