.. _contributing:

Contributing to bitmath
#######################

This section describes the guidelines for contributing to bitmath.

.. contents::
   :depth: 3
   :local:



.. _contributing_code_of_conduct:

Code of Conduct
***************

All persons submitting code or otherwise interacting with the bitmath
project on GitHub must accept and abide by the terms of the `Code of
Conduct
<https://github.com/timlnx/bitmath/blob/master/CODE_OF_CONDUCT.md>`_.


.. _contributing_issue_reporting:

Issue Reporting
***************

If you encounter an issue with the bitmath library, please use the
provided template.

* `Open a new issue <https://github.com/timlnx/bitmath/issues/new>`_
* `View open issues <https://github.com/timlnx/bitmath/issues>`_


.. _contributing_code_style:

Code Style and Formatting
*************************

Two static analysis checks run on every pull request as part of the
GitHub Actions CI workflow, and locally via ``make ci``:

* ``pycodestyle`` — checks code style, with **E501** (line too long)
  and **E722** (bare ``except``) ignored.
* ``flake8 --select=F`` — runs pyflakes error checks only (undefined
  names, unused imports, etc.). Style checks are disabled.

A PR cannot be merged until both pass. Run ``make ci`` locally to
check before submitting.


.. _contributing_commit_messages:

Commit Messages
***************

Please write `intelligent commit messages
<http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.

For example::

   Short summary (50 chars or less)

   More detailed explanatory text, if necessary. Wrap it to about 72
   characters or so.

   Write your commit message in the imperative: "Fix bug" and not
   "Fixed bug" or "Fixes bug."

   - Bullet points are okay, too


.. _contributing_pull_requests:

Pull Requests
*************

When you open a pull request, GitHub Actions automatically runs the
full test suite across all supported Python versions. The repository is
configured to block merges until all checks pass — you don't need to
trigger anything manually.

If a check fails, GitHub will report the failure directly on the pull
request. Review the output, push a fix, and the checks will re-run
automatically.

The bitmath project **welcomes all contributors**. If you're unable to
fix a failing check yourself, leave a comment on the pull request
explaining the situation and we'll help.


.. _contributing_python_versions:

Supported Python Versions
*************************

bitmath supports Python versions shipping with the current and previous
major RHEL release available via `EPEL <https://docs.fedoraproject.org/en-US/epel/>`_.
This means the minimum supported version tracks the oldest Python still
included in a supported EPEL target:

* **RHEL 10 / EPEL 10** — Python 3.12
* **RHEL 9 / EPEL 9** — Python 3.9, 3.11

The CI matrix tests all versions in this range. When a RHEL major
release reaches end-of-life and is dropped from EPEL, the corresponding
Python versions may be dropped from the support matrix in the next
bitmath release.

If anybody wants to take over Debian/Ubuntu patching, we can add notes
for which distributions are covered.


.. _contributing_automated_tests:

Automated Tests
***************

Write `unittests <https://docs.python.org/3/library/unittest.html>`_
for any new functionality if you are up to the task. It is not a hard
requirement, but it greatly helps.

All bitmath code includes unit tests to verify expected functionality.


.. _contributing_components:

Components
==========

The bitmath test suite depends on the following tools:

* `GitHub Actions <https://github.com/timlnx/bitmath/actions>`_ —
  Runs the full test suite automatically on every pull request across
  all supported Python versions.

* `unittest <https://docs.python.org/3/library/unittest.html>`_ —
  Python's standard unit testing framework. All bitmath tests are
  written using this framework.

* `pytest <https://docs.pytest.org/en/latest/>`_ — Test runner used
  to execute the unittest-based test suite, collect results, and report
  coverage.

* `pytest-cov <https://pytest-cov.readthedocs.io/>`_ — Coverage plugin
  for pytest. The project aims for high coverage; reasonable exceptions
  can always be discussed in the pull request.

* `pycodestyle <https://pypi.org/project/pycodestyle/>`_ — Checks
  Python code style.

* `pyflakes <https://pypi.org/project/pyflakes/>`_ — Checks Python
  source files for errors.

* `virtualenv <https://virtualenv.pypa.io/en/latest/>`_ — Creates an
  isolated Python environment. The ``make ci`` target manages this
  automatically.

* `Makefile <http://www.gnu.org/software/make/>`_ — Orchestrates
  all build and test tasks. See :ref:`contributing_makefile_targets`
  below.


.. _contributing_makefile_targets:

Makefile Targets
================

All development tasks are driven through ``make``. The targets most
relevant to contributors are:

.. note::

   These targets are how you test your changes locally and clean up
   afterwards before opening a pull request.

``make ci``
   The primary target. Creates a Python virtualenv, installs all
   dependencies from ``requirements.txt``, runs the unique test name
   check, executes the full pytest suite with coverage, and runs
   ``pycodestyle`` and ``pyflakes``. Run this before opening a pull
   request. **This is the same check GitHub Actions runs.**

``make clean``
   Removes the virtualenv, compiled ``*.pyc`` files, ``__pycache__``
   directories, and build artifacts. Run ``make clean; make ci`` for a
   guaranteed fresh test run.

``make docs``
   Builds the HTML documentation locally using Sphinx. Output is
   written to ``docsite/build/html/``. Run ``make viewdocs`` to open
   the result automatically in your default browser, or open
   ``docsite/build/html/index.html`` directly.


.. _contributing_running_tests:

Running the Tests
=================

The simplest way to run the full test suite locally is:

.. code-block:: console

   $ make ci

For a guaranteed clean run (recommended before opening a PR):

.. code-block:: console

   $ make clean; make ci

The output will look something like this (dependency installation
output omitted for brevity):

.. code-block:: console

   #############################################
   # Running Unique TestCase checker
   #############################################
   ./tests/test_unique_testcase_names.sh

   #############################################
   # Creating a virtualenv
   #############################################
   ... (dependency installation) ...

   #############################################
   # Running Unit Tests
   #############################################
   ============================= test session starts ==============================
   tests/test_arithmetic.py::TestArithmetic::test_add_bitmath_to_bitmath PASSED [  0%]
   tests/test_arithmetic.py::TestArithmetic::test_sub_bitmath_from_bitmath PASSED [  0%]
   ... (hundreds more) ...

   ================================ tests coverage ================================
   Name    Stmts   Miss  Cover   Missing
   -------------------------------------
   TOTAL     623      0   100%

   ======================== NNN passed in Xs ========================

The exact test count grows as new tests are added.

The definitive pass/fail verdict comes from the GitHub Actions workflow
on your pull request, which runs the suite across all supported Python
versions. A clean local ``make ci`` is a strong signal, but the PR
checks are the final authority.
