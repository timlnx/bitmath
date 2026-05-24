# Maintainers

bitmath is a one-person project, and has been since 2014. This file
exists so downstream consumers (and any future contributors) can see
exactly who has the keys to the kingdom and what those keys unlock.

## Current Maintainer

**Tim Case** (GitHub: [@timlnx](https://github.com/timlnx))

* Role: Project lead, sole maintainer
* Contact: `bitmath@lnx.cx`
* Bluesky: [@lnx.cx](https://bsky.app/profile/lnx.cx)
* Homepage: [Technitribe](https://blog.lnx.cx)
* Formerly: Tim Bielawa (`tbielawa`)

## Access to Sensitive Resources

I have admin access to the following resources. Nobody else does.

* The [timlnx/bitmath](https://github.com/timlnx/bitmath) GitHub
  repository (admin role, including the ability to change branch
  protection rules, manage secrets, and modify security settings).
* The `bitmath` project on [PyPI](https://pypi.org/project/bitmath/).
  Publishing happens through PyPI Trusted Publishing (OIDC), so there
  is no long-lived API token to leak. The trust relationship is
  configured in PyPI's web UI and is scoped to the
  `.github/workflows/publish.yml` workflow on the `master` branch.
  PyPI account has 2fa enabled.
* The [bitmath on Read The Docs](https://bitmath.readthedocs.io/)
  documentation project.
* The `bitmath@lnx.cx` email address used for private vulnerability
  reports (see [SECURITY.md](SECURITY.md)).

If you ever see a release on PyPI, a tag pushed to master, or a
security advisory published that did not originate from me, treat it
as a compromise and reach out immediately through any of the contact
channels in [SECURITY.md](SECURITY.md).

## Responsibilities

As the sole maintainer I am responsible for:

* Reviewing and merging pull requests.
* Cutting releases (version bumps, `NEWS.rst` entries, tags, PyPI
  publication via the OIDC workflow).
* Triaging security reports per the timelines in
  [SECURITY.md](SECURITY.md).
* Enforcing the [Code of Conduct](CODE_OF_CONDUCT.md). Note that I am
  both the sole enforcer and the sole maintainer, which means if a
  Code of Conduct concern involves me directly, the project itself
  cannot offer you a neutral venue. Your remedies in that case are
  the usual ones available against any open source maintainer: public
  comment on the issue tracker, a fork, or moving to a different
  library. I would rather be honest about that limitation than
  pretend the project has a governance structure it does not have.
* Keeping the dependency surface honest. bitmath has zero runtime
  dependencies on purpose; development dependencies are listed in
  `requirements.txt`.

## Decision Making

Decisions are made by me, with input solicited from the issue and PR
discussions when the question is non-obvious or has visible downstream
impact. I try to write up the reasoning when something might surprise
people (see commit messages and `NEWS.rst` for the audit trail).

## Becoming a Maintainer

bitmath has not historically had additional maintainers, but the
project has been around for over a decade and I am not immortal. If
you are interested in helping carry this forward, open an issue or
reach out by email. Co-maintainership would start with regularly
landing reviewed contributions and graduate to write access after we
have built up some trust.

### Open Maintainer Request: Debian / Ubuntu Packaging

There is a standing ask tracked in [issue
#117](https://github.com/timlnx/bitmath/issues/117) ("Deb Maintainer
Wanted") and echoed in the [contributing
guide](https://bitmath.readthedocs.io/en/latest/contributing.html#supported-python-versions):
bitmath currently tracks the Python versions shipped in the current
and previous major RHEL releases via EPEL, because that is the
ecosystem I personally pay attention to. There is no official Debian
or Ubuntu release channel right now and I am looking for somebody to
take over `.deb` patching and the related distribution coverage. This
is a real way to get involved without having to take on the entire
project. Comment on #117, email me, or open a fresh issue if you want
to claim the role.

## Inactive Maintainers

None at present.
