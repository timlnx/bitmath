NEWS
####

.. contents::
   :depth: 1
   :local:

.. _bitmath-2.1.0:

bitmath-2.1.0
*************

*Released: May 24, 2026*

bitmath 2.1.0 is a focused follow-up to the 2.0.0 modernization. It
finishes the last of the Python 2 cleanup, tightens the project's
quality tooling, retires one piece of legacy API surface, and works
through OpenSSF's full menu of supply-chain checks (Scorecard, Best
Practices, and the OSPS Baseline) to put a credible security posture
on the record. The public API is essentially unchanged from 2.0; the
two breaking changes below are narrow ones that affect internal-type
inspection and one deprecated helper.


Breaking Changes
================

**Internal representation is uniformly floating-point**
   Every bitmath instance now stores its size as a 64-bit float, no
   matter which constructor created it. Previously the ``bytes=`` and
   ``bits=`` keyword constructors, along with the bit-family value
   constructors such as ``Kib(N)``, leaked Python ``int`` values
   through the ``.bytes`` and ``.bits`` properties. Those properties
   now always return ``float``, matching the long-documented
   floating-point measurement design described in the :ref:`Rules for
   Math <appendix_math>` appendix. Equality, ordering, ``repr()``, and
   arithmetic results are unchanged; only code that inspected
   ``type(instance.bytes)`` or ``type(instance.bits)`` directly will
   observe the difference.

**listdir() is deprecated**
   :func:`bitmath.listdir` now emits a :exc:`DeprecationWarning` on
   every call and will be removed in a future release. Iterate with
   :py:func:`os.walk` and call :func:`bitmath.getsize` directly
   instead. Closes `issue #27
   <https://github.com/timlnx/bitmath/issues/27>`_.


Library Improvements
====================

**pathlib support**
   :func:`bitmath.getsize` now accepts :class:`pathlib.Path` objects,
   not just strings, for its ``path`` argument.


Project Infrastructure
======================

**Linting moved to pylint**
   pylint replaces flake8/pyflakes across the CI workflow and the
   local toolchain, and the library is held at a 10.00/10 score.
   pycodestyle is retained for the PEP 8 whitespace checks pylint
   does not cover.

**Security scanning with bandit**
   Bandit is a static analyzer from PyCQA that scans Python source
   for common security smells (hardcoded secrets, ``eval``,
   ``subprocess`` calls with ``shell=True``, insecure ``yaml`` and
   ``pickle`` deserialization, weak crypto primitives). It runs as
   part of ``make ci`` and as a dedicated GitHub Actions workflow
   that fires on every push, every pull request, and on a weekly
   schedule, scanning both ``bitmath/`` and ``tests/``.

**100% test coverage**
   The remaining coverage gaps were closed, including the
   platform-specific :func:`bitmath.query_device_capacity` branches,
   bringing the suite to 100% measured coverage on every supported
   platform.

**Property-based testing with Hypothesis**
   Four ``@given`` properties cover :func:`bitmath.parse_string`
   roundtrips, lossless unit conversion across every ``(src, dst)``
   pair in :data:`bitmath.ALL_UNIT_TYPES`, and the contract that
   :func:`bitmath.parse_string` raises only :exc:`ValueError` on bad
   input. The roundtrip property already turned up a real parser bug
   around scientific-notation float formatting, which is filed as a
   follow-up. See `PR #144
   <https://github.com/timlnx/bitmath/pull/144>`_.

**SPDX license headers**
   Every source and test file now carries ``SPDX-License-Identifier``
   and ``SPDX-FileCopyrightText`` headers.

**Single-sourced version**
   The package version is read dynamically from the ``VERSION`` file
   by hatchling, so bumping that one file propagates everywhere.

**Signed releases (landing with 2.1.0)**
   The 2.1.0 release closes out the open OSSF Scorecard
   Signed-Releases finding ("Determines if the project
   cryptographically signs release artifacts," currently flagged
   at high severity). Scorecard should reflect the improvement on
   its next weekly run after the release lands.


Security and Supply Chain
=========================

.. |scorecard| image:: https://api.securityscorecards.dev/projects/github.com/timlnx/bitmath/badge
   :target: https://securityscorecards.dev/viewer/?uri=github.com/timlnx/bitmath
   :alt: OSSF Scorecard
.. |bestpractices| image:: https://www.bestpractices.dev/projects/12749/badge
   :target: https://www.bestpractices.dev/en/projects/12749
   :alt: OpenSSF Best Practices
.. |baseline| image:: https://www.bestpractices.dev/projects/12749/baseline
   :target: https://www.bestpractices.dev/projects/12749
   :alt: OpenSSF Baseline

|scorecard| |bestpractices| |baseline|

Most of the work in this release happened here. OpenSSF's
supply-chain story has matured enough to be worth pursuing in earnest
even on a small library like bitmath, and the project now carries
the badges and the automation to back them up.

**OpenSSF Best Practices passing badge**
   bitmath earned the `OpenSSF Best Practices passing badge
   <https://www.bestpractices.dev/projects/12749>`_. The full
   self-assessment is on the linked profile; the badge appears on the
   README and the docsite landing page alongside the OSSF Scorecard
   and OSPS Baseline badges.

**OSPS Baseline Levels 1 and 2 (Level 3 mostly)**
   `OSPS Baseline <https://baseline.openssf.org/>`_ Level 1: 23 Met,
   2 Not Applicable, 0 Unmet. Level 2: 19 Met, 0 Unmet. Level 3: 18
   Met, 2 Not Applicable, 1 Unmet. The single Unmet at Level 3 is
   OSPS-QA-07.01 (non-author code review), which is structurally
   blocked by this being a single-maintainer project. Closing it
   would require either onboarding a second maintainer or changing
   the project governance model, neither of which is happening in
   2.1.0. The control responses backing each Met assessment live in
   the docsite under :ref:`Project Architecture
   <contributing_architecture>` and the policy documents listed below.

**OSSF Scorecard**
   ``.github/workflows/scorecard.yml`` runs on every push to
   ``master``, on branch-protection-rule changes, and on a weekly
   cron. Current score and history are published at
   https://securityscorecards.dev/viewer/?uri=github.com/timlnx/bitmath.

**GitHub Actions pinned to commit SHAs**
   Every GitHub Actions reference in ``.github/workflows/`` is now
   pinned to a full-length commit SHA with the version as a trailing
   ``# vX.Y.Z`` comment. Floating tags (the old ``@v4``) and
   floating branch refs (the now-removed
   ``MishaKav/pytest-coverage-comment@main`` third-party step) are
   gone. Dependabot keeps the SHAs fresh.

**Dependabot**
   ``.github/dependabot.yml`` watches the ``github-actions`` and
   ``pip`` ecosystems on a weekly cadence. Minor and patch bumps are
   grouped per ecosystem to keep PR noise bounded; major bumps land
   as standalone PRs so breaking-change review stays honest.

**Hardened workflow token permissions**
   Every workflow declares an explicit ``permissions: read-all`` at
   the top level, with ``write`` scopes applied only to the jobs that
   need them (``security-events: write`` for SARIF upload,
   ``id-token: write`` for PyPI OIDC Trusted Publishing, and so on).
   The default-write ``GITHUB_TOKEN`` posture is no longer inherited
   anywhere.

**SCA via pip-audit**
   ``.github/workflows/sca.yml`` runs `pip-audit
   <https://github.com/pypa/pip-audit>`_ on every push, every pull
   request, and on a weekly cron. bitmath has no runtime
   dependencies, so this scans the test-only deps in
   ``requirements.txt``. Findings are resolved on the release-blocking
   timetable specified in ``SECURITY_POLICIES.md``.

**CycloneDX SBOM attached to every release**
   The publish workflow now installs the built wheel into an isolated
   venv, snapshots it with `cyclonedx-py
   <https://github.com/CycloneDX/cyclonedx-python>`_, and attaches
   the resulting ``bitmath-<version>.cdx.json`` to the GitHub release
   alongside the wheel and sdist. Downstream consumers who SBOM-scan
   everything they ingest can now pull bitmath's SBOM from the
   release page directly instead of generating their own.


Project Documentation and Governance
====================================

The documentation set picked up five new top-level files this
release. These exist to answer standing security, governance, and
verification questions for downstream consumers without requiring a
real-time email exchange, and several of them are direct deliverables
for OSPS Baseline controls.

`MAINTAINERS.md <https://github.com/timlnx/bitmath/blob/master/MAINTAINERS.md>`_
   New top-level file naming the sole current maintainer, the
   sensitive-resource access that comes with the role (PyPI account,
   GitHub admin, GPG key, ReadTheDocs admin), maintainer
   responsibilities, and a standing open call for a Debian/Ubuntu
   co-maintainer (see `issue #117
   <https://github.com/timlnx/bitmath/issues/117>`_ if you're
   interested).

`ARCHITECTURE.md <https://github.com/timlnx/bitmath/blob/master/ARCHITECTURE.md>`_
   New top-level design document covering runtime architecture, the
   build and release pipeline (including the Packit downstream RPM
   flow into Fedora and EPEL), CI gates, trust boundaries, and the
   documentation pipeline. Lives at the repo root so the OpenSSF
   scanner finds it by filename, and so anyone exploring the repo for
   the first time can get the design picture before reading code.

`SECURITY_ASSESSMENT.md <https://github.com/timlnx/bitmath/blob/master/SECURITY_ASSESSMENT.md>`_
   Standing threat model describing the attack surfaces (supply
   chain, PyPI account, source repository, build chain, distribution
   chain), the mitigations in place for each, and the automated
   security tooling stack with what each tool catches.

`SECURITY_POLICIES.md <https://github.com/timlnx/bitmath/blob/master/SECURITY_POLICIES.md>`_
   The SAST and SCA remediation thresholds and release-blocking
   criteria in one place. Bandit and pip-audit findings, severity
   ladder, the rule for what blocks a release versus what gets a
   follow-up, and the timetable for acting on each.

`VERIFICATION.md <https://github.com/timlnx/bitmath/blob/master/VERIFICATION.md>`_
   Downstream-consumer guide for verifying a bitmath release end to
   end: integrity via the SHA-256 sums published alongside the GitHub
   release, authenticity via `PEP 740
   <https://peps.python.org/pep-0740/>`_ attestations and
   `pypi-attestations
   <https://github.com/trailofbits/pypi-attestations>`_, and
   provenance via the CycloneDX SBOM. If your organization's policy
   requires verifying every dependency before installation, this is
   the playbook.

`SECURITY.md <https://github.com/timlnx/bitmath/blob/master/SECURITY.md>`_ tightened up
   Coordinated Vulnerability Disclosure now states explicit response
   timeframes (72 hours to acknowledge a report, 7 days to triage),
   and the document picked up new Scope of Support, Duration of
   Support, and Secrets and Credentials Policy sections.

**HTTPS for all project doc URLs**
   Every ``http://`` reference to project-owned documentation
   (``bitmath.readthedocs.io``, the docsite, README badge targets,
   NEWS historical links, CONTRIBUTING) has been switched to
   ``https://`` to clear the bestpractices.dev ``sites_https`` check.
   ReadTheDocs was already serving TLS; only the scheme needed
   flipping. See `PR #146
   <https://github.com/timlnx/bitmath/pull/146>`_.


.. _bitmath-2.0.0:

bitmath-2.0.0
*************

*Released: April 25, 2026*

Nearly eight years after 1.3.3 shipped in 2018, bitmath is back with
a major release. Version 2.0.0 is a thorough modernization: the
Python 2 era is officially over, the library picks up several
long-requested features, and the entire project infrastructure has
been rebuilt from scratch. If you've been running bitmath on Python
3.9 or later and quietly wishing it felt more modern — this release
is for you.

Check over on `my blog
<https://blog.lnx.cx/2026/04/25/bitmath-2.0.0-finally-released.html>`_
for a personal recap of this release, how much it means to me, and
what it took to get here.


Breaking Changes
================

**Python support**
   Python 3.9+ only. Python 2 and Python < 3.9 are no longer
   supported or tested.

**parse_string() default system**
   The default unit system when ``strict=False`` is now **NIST** (base-2).
   Previously it defaulted to SI (base-10). Code that relied on the old default
   for ambiguous strings such as ``"1g"`` could get a different result. See
   :ref:`parse-string-non-strict` for full details. All bitmath now consistently
   defaults to the NIST system.

**parse_string_unsafe() deprecated**
   Use :func:`bitmath.parse_string` with ``strict=False`` instead.
   The old name still works but emits a :exc:`DeprecationWarning`.

**bitmath.integrations removed**
   The ``argparse``, ``click``, and ``progressbar`` integrations have been removed
   from the package. Copy-paste replacements are provided in the new
   :ref:`Integration Examples <integration_examples>` documentation
   chapter. No changes to calling code are required — just a local
   copy of the relevant snippet.

**Byte and Bit display names**
   ``Byte`` and ``Bit`` now display as ``B`` and ``b`` respectively,
   matching the abbreviated style of every other unit. Code that
   compares formatted strings (e.g. ``"{unit}"`` in a format template
   or the output of ``str()`` / ``repr()``) against the literal words
   ``"Byte"`` or ``"Bit"`` will need to be updated. The class names
   themselves are unchanged.

**query_device_capacity() on macOS**
   :func:`bitmath.query_device_capacity` now raises
   :exc:`NotImplementedError` on macOS. System Integrity Protection
   (SIP) blocks raw block device access even for root, making the
   previous ioctl path unreliable. Use :func:`bitmath.query_capacity`
   instead.

**Build and install**
   ``setup.py`` and ``setup.py.in`` are gone. Installation is
   ``pip install bitmath``. Source builds use ``python -m build``.



Library Improvements
====================

The core API is unchanged — every bitmath object you created before
still works exactly the same way. What 2.0.0 adds on top of that:

**Full NIST unit coverage**
   The four largest NIST prefix units — :class:`~bitmath.ZiB`,
   :class:`~bitmath.YiB`, :class:`~bitmath.Zib`, and
   :class:`~bitmath.Yib` — are now first-class bitmath types. All
   constants (:ref:`NIST_PREFIXES, NIST_STEPS, ALL_UNIT_TYPES
   <module_class_variables>`) reflect reality.

**f-string and format() support**
   bitmath objects now implement the Python format protocol
   (``__format__``, `PEP 3101 <https://peps.python.org/pep-3101/>`_). They can be used directly in f-strings
   with format specs — ``f"{some_size:.2f}"`` just works. See
   :ref:`instances_dunder_format` for the full reference. Credit to
   `Jonathan Eunice <https://github.com/jonathaneunice>`_ for the
   original concept in `PR #76
   <https://github.com/timlnx/bitmath/pull/76>`_.

**bitmath.sum() and built-in sum()**
   A new :func:`bitmath.sum` function returns a unit-normalized result
   when summing mixed-type iterables. For uniform collections, the
   built-in :py:func:`sum` now works directly on bitmath sequences
   without a ``start=`` argument.

**Thread-safe context manager**
   The :func:`bitmath.format` context manager previously mutated
   module-level globals, making it unsafe under concurrent access. It
   now uses ``threading.local`` with proper save/restore semantics,
   including correct nesting behavior. Closes `issue #83
   <https://github.com/timlnx/bitmath/issues/83>`_.

**best_prefix() bit-family fix**
   :func:`bitmath.best_prefix` incorrectly converted bit-family units
   (e.g. ``Kib``) into byte-family units (e.g. ``KiB``). The unit
   family is now preserved. Closes `issue #95
   <https://github.com/timlnx/bitmath/issues/95>`_.

**query_capacity() — recommended volume size API**
   New :func:`bitmath.query_capacity` returns a :class:`bitmath.Capacity`
   NamedTuple of ``(total, used, free)`` :class:`bitmath.Bitmath`
   instances for any path or mount point. Works cross-platform without
   elevated privileges. This is the recommended API for "how big is
   this volume?" queries. Accepts ``bestprefix=True`` (default) to get
   already human-readable units (e.g. ``GiB``) and ``system=bitmath.SI``
   to opt into decimal prefixes instead of the default NIST binary
   prefixes. Set ``bestprefix=False`` to receive raw
   :class:`bitmath.Byte` instances.

**Windows device capacity**
   :func:`bitmath.query_device_capacity` now works on Windows via
   ``DeviceIoControl``. Open the device as
   ``open(r'\\.\PhysicalDrive0', 'rb')`` (administrator privileges
   required). Unsupported platforms raise :exc:`NotImplementedError`.
   The new :data:`bitmath.SUPPORTED_PLATFORMS` constant lists all
   platforms where the function is available. Closes `issue #52
   <https://github.com/timlnx/bitmath/issues/52>`_.

**query_device_capacity() Linux buffer fix**
   :func:`bitmath.query_device_capacity` on Linux was passing an
   integer where an ioctl buffer was required, causing
   ``OSError: [Errno 14] Bad address``. The call now correctly
   allocates a zero-filled buffer of the proper size via
   ``b'\\x00' * struct.calcsize(fmt)``.

**Flexible string parsing**
   :func:`bitmath.parse_string` with ``strict=False`` accepts
   ambiguous input such as ``"1g"`` or ``"1GB"`` and resolves it to
   the most likely unit. When the system cannot be reliably determined,
   NIST is the tiebreaker. Closes `issue #54
   <https://github.com/timlnx/bitmath/issues/54>`_.

**Floor division, modulo, and divmod for capacity math**
   bitmath objects now implement ``__floordiv__`` (``//``),
   ``__mod__`` (``%``), and ``__divmod__`` — useful for
   chunk-and-remainder capacity planning (*"how many N-sized chunks
   fit into this device, and how much is left over?"*).
   ``bm1 // bm2`` returns an ``int`` (count of whole divisions),
   mirroring how ``bm1 / bm2`` returns a unitless ratio.
   ``bm1 % bm2`` and ``divmod(bm1, bm2)`` return remainders as
   bitmath objects of the **left-hand operand's type**, consistent
   with every other bitmath arithmetic operator. The identity
   ``(a // b) * b + (a % b) == a`` holds. See :ref:`capacity_math`
   for worked examples including ``best_prefix()`` coercion and
   ``bitmath.format`` context-manager integration.


Project Infrastructure
======================

The project infrastructure has been rebuilt to reflect how Python
projects are actually maintained in 2026:

**Project Security**
   GitHub now has branch protection enabled. Releases are signed with
   the maintainers `GPG key
   <https://keys.openpgp.org/search?q=bitmath%40lnx.cx>`_.

**Packaging**
   ``pyproject.toml`` with a hatchling backend replaces the old
   ``setup.py``/``setup.py.in`` template system. The package is
   `PEP 517 <https://peps.python.org/pep-0517/>`_/`PEP 518
   <https://peps.python.org/pep-0518/>`_ compliant. ``MANIFEST.in``
   is gone; sdist content is declared explicitly in
   ``pyproject.toml``.

**GitHub Actions**
   CI now runs against Python 3.9 through 3.13 on Ubuntu, macOS, and
   Windows, with actions pinned to current versions (``checkout@v6``,
   ``setup-python@v5``). Tests run on every pull request, not just
   pushes.

**Security scanning**
   CodeQL analysis runs on every push to master, every pull request,
   and on a weekly schedule.

**ReadTheDocs**
   ``.readthedocs.yaml`` is now present and explicit. The RTD build
   uses Python 3.11 and installs ``sphinx_rtd_theme`` directly.

**Development workflow**
   ``make ci`` is the single command for a full local build: unique
   test name check, pycodestyle, flake8, and pytest with coverage.
   ``make build``, ``make pypitest``, and ``make pypi`` replace the
   old ``make sdist upload`` pattern.

**Fedora/EPEL**
   Expect to see fresh builds in Fedora/EPEL over the coming
   weeks. Hopefully I can sneak this into EPEL 10, EPEL 9 might be
   picky since this is a major version change.


Closing Thoughts
================

bitmath started as a small passion project of mine. A utility for
thinking about and clearly expressing file sizes, and that's still
exactly what it is. This 2.0.0 release doesn't change what the library
does. What I've done is change the very foundation that it's built
on. The test suite measures in at 311 tests now, basically 100%
coverage when you add all the platform-specific checks together. The
documentation has been comprehensively reviewed and updated. The
packaging is modernized.

It really is a remarkable milestone in project history. I have to give
the warmest thanks to all of the users and fans who have written bug
reports and submitted pull requests. Especially in the least active
years of the project. Most of those PRs and Issues have been
integrated into this massive 2.0.0 release.

**Thanks for your patience and your participation.**

If you've been holding off on adopting bitmath because the last
release predated your Python version — yeah I totally get it. This
place was a dumpster for the last 8 years.

Go on, give it a shot. It really is better than ever.


.. _bitmath-1.4.0-1:

bitmath-1.4.0-1
***************

bitmath-1.4.0 was published on 2026-04-16.


Project
=======

Version 1.4.0 is a maintenance release — the final release to support
Python 2 era packaging infrastructure. It addresses two long-standing
issues and makes no breaking changes.


Changes
=======

**Bug Fixes**

* Fixed packaging: ``bitmath.integrations`` subpackage was missing from
  the ``packages`` list in ``setup.py.in``, causing the argparse, click,
  and progressbar integrations to be absent from installed distributions.
  Reported in `PR #107 <https://github.com/tbielawa/bitmath/pull/107>`_.

* Modernized mock imports in the test suite: ``tests/test_progressbar.py``
  and ``tests/test_query_device_capacity.py`` now prefer ``unittest.mock``
  (stdlib, Python 3.3+) and fall back to the third-party ``mock`` package.
  Based on `PR #105 <https://github.com/tbielawa/bitmath/pull/105>`_.


.. _bitmath-1.3.3-1:

bitmath-1.3.3-1
***************

`bitmath-1.3.3-1
<https://github.com/timlnx/bitmath/releases/tag/1.3.3.1>`__ was
published on 2018-08-23.


Project
=======

Version 1.3.3 is a minor update primarily released to synchronize
versions across platforms. Additionally there are small packaging
updates to keep up with changing standards.

Minor bug fixes and documentation tweaks are included as well.

The project now has an official `Code of Conduct
<https://github.com/timlnx/bitmath/blob/master/CODE_OF_CONDUCT.md>`_,
as well as issue and pull request templates.


What happened to bitmath 1.3.2? It only ever existed as an idea in
source control.


Changes
=======

**Bug Fixes**

`Alexander Kapshuna <https://github.com/kapsh>`_ has submitted
`several fixes
<https://github.com/timlnx/bitmath/pulls?q=is%3Apr+author%3Akapsh>`_
since the last release. Thanks!

* Packaging requirements fixes
* Python 3 compatibility
* Subclassing and Type checking fixes/improvements

`Marcus Kazmierczak <https://github.com/mkaz>`_ submitted `a fix
<https://github.com/timlnx/bitmath/pull/75>`_ for some broken
documentation links.

And `Dawid Gosławski <https://github.com/alkuzad>`_ make sure our
`documentation <https://github.com/timlnx/bitmath/pull/62/files>`_
is accurate.


Thanks to all the bitmath contributors over the years!


.. _bitmath-1.3.1-1:

bitmath-1.3.1-1
***************

`bitmath-1.3.1-1
<https://github.com/timlnx/bitmath/releases/tag/1.3.1.1>`__ was
published on 2016-07-17.

Changes
=======

**Added Functionality**

* New function: :func:`bitmath.parse_string_unsafe`, a less strict
  version of :func:`bitmath.parse_string`. Accepts inputs using
  *non-standard* prefix units (such as single-letter, or
  mis-capitalized units).

* Inspired by `@darkblaze69 <https://github.com/darkblaze69>`_'s
  request in `#60 "Problems in parse_string"
  <https://github.com/timlnx/bitmath/issues/60>`_.


Project
=======

**Ubuntu**

* Bitmath is now available for installation via Ubuntu Xenial, Wily,
  Vivid, Trusty, and Precise PPAs.

* Ubuntu builds inspired by `@hkraal <https://github.com/hkraal>`_
  reporting an `installation issue
  <https://github.com/timlnx/bitmath/issues/57>`_ on Ubuntu systems.


**Documentation**

* `Cleaned up a lot <https://github.com/timlnx/bitmath/issues/59>`_
  of broken or re-directing links using output from the Sphinx ``make
  linkcheck`` command.


.. _bitmath-1.3.0-1:

bitmath-1.3.0-1
***************

`bitmath-1.3.0-1
<https://github.com/timlnx/bitmath/releases/tag/1.3.0.1>`__ was
published on 2016-01-08.

Changes
=======

**Bug Fixes**

* Closed `GitHub Issue #55
  <https://github.com/timlnx/bitmath/issues/55>`_ "best_prefix for
  negative values". Now :func:`bitmath.best_prefix` returns correct
  prefix units for negative values. Thanks `mbdm
  <https://github.com/mbdm>`_!


.. _bitmath-1.2.4-1:

bitmath-1.2.4-1
***************

`bitmath-1.2.4-1
<https://github.com/timlnx/bitmath/releases/tag/1.2.4-1>`__ was
published on 2015-11-30.

Changes
=======

**Added Functionality**

* New bitmath module function: :func:`bitmath.query_device_capacity`. Create
  :class:`bitmath.Byte` instances representing the capacity of a block
  device. Support is presently limited to Linux and Mac.

* The :func:`bitmath.parse_string` function now can parse 'octet'
  based units. Enhancement requested in `#53 parse french unit names
  <https://github.com/timlnx/bitmath/issues/53>`_ by `walidsa3d
  <https://github.com/walidsa3d>`_.

**Bug Fixes**

* `#49 <https://github.com/timlnx/bitmath/pull/49>`_ - Fix handling
  unicode input in the `bitmath.parse_string
  <https://bitmath.readthedocs.io/en/latest/module.html#bitmath-parse-string>`__
  function. Thanks `drewbrew <https://github.com/drewbrew>`_!

* `#50 <https://github.com/timlnx/bitmath/pull/50>`_ - Update the
  ``setup.py`` script to be python3.x compat. Thanks `ssut
  <https://github.com/ssut>`_!


Documentation
=============

* The project documentation is now installed along with the bitmath
  library in RPM packages.


Project
=======

**Fedora/EPEL**

Look for separate python3.x and python2.x packages coming soon to
`Fedora <https://getfedora.org/>`_ and `EPEL
<https://fedoraproject.org/wiki/EPEL>`_. This is happening because of
the `initiative
<https://fedoraproject.org/wiki/FAD_Python_3_Porting_2015>`_ to update
the base Python implementation on Fedora to Python 3.x

* `BZ1282560 <https://bugzilla.redhat.com/show_bug.cgi?id=1282560>`_



.. _bitmath-1.2.3-1:

bitmath-1.2.3-1
***************

`bitmath-1.2.3-1
<https://github.com/timlnx/bitmath/releases/tag/1.2.3-1>`__ was
published on 2015-01-03.

Changes
=======

**Added Functionality**

* New utility: ``progressbar`` integration:
  `bitmath.integrations.BitmathFileTransferSpeed
  <https://bitmath.readthedocs.io/en/latest/module.html#progressbar>`_.
  A more functional file transfer speed widget.


Documentation
=============

* The command-line ``bitmath`` tool now has `online documentation
  <https://bitmath.readthedocs.io/en/latest/commandline.html>`_
* A full demo of the ``argparse`` and ``progressbar`` integrations has
  been written. Additionally, it includes a comprehensive
  demonstration of the full capabilities of the bitmath library. View
  it in the *Real Life Demos* `Creating Download Progress Bars
  <https://bitmath.readthedocs.io/en/latest/real_life_examples.html#real-life-examples-download-progress-bars>`_
  example.


Project
=======

**Tests**

* Travis-CI had some issues with installing dependencies for the 3.x
  build unittests. These were fixed and the build status has returned
  back to normal.


.. _bitmath-1.2.0-1:

bitmath-1.2.0-1
***************

`bitmath-1.2.0-1
<https://github.com/timlnx/bitmath/releases/tag/1.2.0-1>`__ was
published on 2014-12-29.

Changes
=======

**Added Functionality**

* New utility: ``argparse`` integration: `bitmath.BitmathType
  <https://bitmath.readthedocs.io/en/latest/module.html#argparse>`_.
  Allows you to specify arguments as bitmath types.

Documentation
=============

* The command-line ``bitmath`` tool now has a `proper manpage
  <https://github.com/timlnx/bitmath/blob/master/bitmath.1.asciidoc.in>`_

Project
=======

**Tests**

* The command-line ``bitmath`` tool is now properly unittested. Code
  coverage back to ~100%.


.. _bitmath-1.1.0-0:

bitmath-1.1.0-1
***************

`bitmath-1.1.0-1
<https://github.com/timlnx/bitmath/releases/tag/1.1.0-1>`_ was
published on 2014-12-20.

* `GitHub Milestone Tracker for 1.1.0 <https://github.com/timlnx/bitmath/milestones/1.1.0>`_

Changes
=======

**Added Functionality**

* New ``bitmath`` `command-line tool
  <https://github.com/timlnx/bitmath/issues/35>`_ added. Provides
  CLI access to basic unit conversion functions
* New utility function `bitmath.parse_string
  <https://bitmath.readthedocs.io/en/latest//module.html#bitmath-parse-string>`_
  for parsing a human-readable string into a bitmath object. `Patch
  submitted <https://github.com/timlnx/bitmath/pull/42>`_ by new
  contributor `tonycpsu <https://github.com/tonycpsu>`_.

.. _bitmath-1.0.8-1:

bitmath-1.0.5-1 through 1.0.8-1
*******************************

`bitmath-1.0.8-1
<https://github.com/timlnx/bitmath/releases/tag/1.0.8-1>`__ was
published on 2014-08-14.

* `GitHub Milestone Tracker for 1.0.8 <https://github.com/timlnx/bitmath/issues?q=milestone%3A1.0.8>`_

Major Updates
=============

* bitmath has a proper documentation website up now on Read the Docs,
  check it out: `bitmath.readthedocs.io
  <https://bitmath.readthedocs.io/en/latest/>`_
* bitmath is now Python 3.x compatible
* bitmath is now included in the `Extra Packages for Enterprise Linux
  <https://fedoraproject.org/wiki/EPEL>`_ EPEL6 and EPEL7 repositories
  (`pkg info
  <https://src.fedoraproject.org/rpms/python-bitmath>`_)
* merged 6 `pull requests
  <https://github.com/timlnx/bitmath/pulls?q=is%3Apr+closed%3A%3C2014-08-28>`_
  from 3 `contributors
  <https://github.com/timlnx/bitmath/graphs/contributors>`_

Bug Fixes
=========

* fixed some math implementation bugs

  * `commutative multiplication <https://github.com/timlnx/bitmath/issues/18>`_
  * `true division <https://github.com/timlnx/bitmath/issues/2>`_

Changes
=======

**Added Functionality**

* `best-prefix
  <https://bitmath.readthedocs.io/en/latest/instances.html#best-prefix>`_
  guessing: automatic best human-readable unit selection
* support for `bitwise operations
  <https://bitmath.readthedocs.io/en/latest/simple_examples.html#bitwise-operations>`_
* `formatting customization
  <https://bitmath.readthedocs.io/en/latest/instances.html#format>`_
  methods (including plural/singular selection)
* exposed many more `instance attributes
  <https://bitmath.readthedocs.io/en/latest/instances.html#instances-attributes>`_
  (all instance attributes are usable in custom formatting)
* a `context manager
  <https://bitmath.readthedocs.io/en/latest/module.html#bitmath-format>`_
  for applying formatting to an entire block of code
* utility functions for sizing `files
  <https://bitmath.readthedocs.io/en/latest/module.html#bitmath-getsize>`_
  and `directories
  <https://bitmath.readthedocs.io/en/latest/module.html#bitmath-listdir>`_
* add `instance properties
  <https://bitmath.readthedocs.io/en/latest/instances.html#instance-properties>`_
  equivalent to ``instance.to_THING()`` methods

Project
=======

**Tests**

* Test suite is now implemented using `Python virtualenv's
  <https://github.com/timlnx/bitmath/blob/master/Makefile#L177>`_
  for consistency across across platforms
* Test suite now contains 150 unit tests. This is **110** more tests
  than the previous major release (`1.0.4-1 <bitmath-1.0.4-1>`__)
* Test suite now runs on EPEL6 and EPEL7
* `Code coverage
  <https://coveralls.io/github/tbielawa/bitmath>`_ is stable
  around 95-100%


.. _bitmath-1.0.4-1:

bitmath-1.0.4-1
***************

This is the first release of **bitmath**. `bitmath-1.0.4-1
<https://github.com/timlnx/bitmath/releases/tag/1.0.4-1>`__ was
published on 2014-03-20.

Project
=======

Available via:

* `PyPi <https://pypi.python.org/pypi/bitmath/>`_
* Fedora 19
* Fedora 20

bitmath had been under development for 12 days when the 1.0.4-1
release was made available.

Debut Functionality
===================

* Converting between **SI** and **NIST** prefix units (``GiB`` to ``kB``)
* Converting between units of the same type (SI to SI, or NIST to NIST)
* Basic arithmetic operations (subtracting 42KiB from 50GiB)
* Rich comparison operations (``1024 Bytes == 1KiB``)
* Sorting
* Useful *console* and *print* representations
