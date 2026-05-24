# bitmath Architecture

> This document exists to satisfy the OSPS Baseline Level 2 control
> [OSPS-SA-01.01](https://www.bestpractices.dev/en/projects/12749/baseline-2)
> (design documentation showing the actions and actors within the
> system), in addition to being useful for downstream consumers and
> contributors who want to understand how bitmath fits together.

## Contents

- [Why This Document Exists](#why-this-document-exists)
- [Runtime Architecture](#runtime-architecture)
- [Build and Release Pipeline](#build-and-release-pipeline)
- [CI and Quality Gates](#ci-and-quality-gates)
- [Trust Boundaries](#trust-boundaries)
- [Documentation Pipeline](#documentation-pipeline)
- [Maintenance](#maintenance)

## Why This Document Exists

This is the architecture map for bitmath. It exists so downstream
consumers and future contributors can see, in one place, what the
moving parts are and how they fit together. It covers two things: the
runtime library (what runs in your process when you `import bitmath`),
and the build and release pipeline (how that code gets from this
repository onto your machine).

It does not cover everything in the repository. Other concerns have
their own homes:

* [MAINTAINERS.md](MAINTAINERS.md): who has access to what.
* [SECURITY.md](SECURITY.md): how to report a vulnerability.
* [SECURITY_ASSESSMENT.md](SECURITY_ASSESSMENT.md): the standing
  threat model.
* [bitmath on Read The Docs](https://bitmath.readthedocs.io/): API
  reference and tutorials.

If you are wondering whether to update this file: yes, if you are
adding a new public function, restructuring the class hierarchy,
changing the build backend, or changing how releases get published.
No, if you are fixing a bug or adding a test.

## Runtime Architecture

### Component Inventory

The runtime library is a single Python module, `bitmath`, deliberately
kept small. Almost all the logic lives in `bitmath/__init__.py`. The
actors that show up at runtime:

| Actor | Lives at | What it does |
|-------|----------|--------------|
| User code | The consumer's process | Imports bitmath, calls module-level functions, instantiates unit classes, does arithmetic |
| Public module API | `bitmath.*` | Module-level entry points: `parse_string`, `parse_string_unsafe`, `best_prefix`, `getsize`, `listdir` (deprecated in 2.1.0), `query_capacity`, `query_device_capacity` |
| `Bitmath` base class | `bitmath.Bitmath` | The arithmetic, comparison, bitwise, and formatting engine. Every concrete unit class inherits from it |
| `Byte` family | `bitmath.Byte`, `KiB`, `MiB`, `GiB`, `TiB`, `PiB`, `EiB`, `kB`, `MB`, `GB`, `TB`, `PB`, `EB`, `ZB`, `YB` | Byte-based concrete unit classes (NIST binary and SI decimal) |
| `Bit` family | `bitmath.Bit`, `Kib`, `Mib`, `Gib`, `Tib`, `Pib`, `Eib`, `kb`, `Mb`, `Gb`, `Tb`, `Pb`, `Eb`, `Zb`, `Yb` | Bit-based concrete unit classes (NIST binary and SI decimal) |
| Constants | `bitmath.NIST`, `bitmath.SI`, `bitmath.NIST_PREFIXES`, `bitmath.SI_PREFIXES`, `bitmath.ALL_UNIT_TYPES` | Module-level lookup tables and system identifiers |
| OS abstraction layer | Standard library: `shutil`, `os`, `fcntl` (Linux), `ctypes` (Windows) | Platform-specific calls used by the capacity-query functions |

### Layered View

```
+--------------------------------------------------------------+
|  User code                                                   |
|    import bitmath; KiB(1024).MiB                             |
+--------------------------------------------------------------+
                          |
                          v
+--------------------------------------------------------------+
|  Public module API (bitmath.*)                               |
|    parse_string, best_prefix, getsize, query_capacity, etc.  |
+--------------------------------------------------------------+
                          |
                          v
+--------------------------------------------------------------+
|  Library core                                                |
|    Bitmath base class                                        |
|      Byte family (KiB, MiB, kB, MB, ...)                     |
|      Bit  family (Kib, Mib, kb, Mb,  ...)                    |
|      _norm_value: normalize every value to bits internally   |
+--------------------------------------------------------------+
                          |
                          v   (only for getsize / listdir /
                          |    query_capacity /
                          |    query_device_capacity)
+--------------------------------------------------------------+
|  OS abstraction layer                                        |
|    shutil.disk_usage   -- cross-platform capacity            |
|    fcntl.ioctl         -- Linux block device capacity        |
|    ctypes / Win32 API  -- Windows block device capacity      |
|    macOS: NotImplementedError (System Integrity Protection)  |
+--------------------------------------------------------------+
```

### Actions

The things that happen at runtime, in roughly the order a typical
consumer triggers them:

1. **Construction.** A user creates a bitmath instance (`KiB(1024)`,
   `Byte(bits=8192)`, `parse_string("4.5 GiB")`). The constructor
   passes the value through `_norm_value`, which converts everything
   to an internal bits representation using the class-level
   `_base_value` and `_unit_value` constants. After construction, the
   instance carries one canonical value.

2. **Conversion.** A user requests a different unit
   (`KiB(1024).MiB`). Each unit class exposes properties that compute
   their own value from the internal bits representation. No
   conversion is cached; every property access does the math fresh.

3. **Arithmetic.** Operators (`+`, `-`, `*`, `/`, `//`, `%`,
   `divmod`) operate on the internal bits representation and return
   a new instance. Mixed-unit arithmetic (`KiB(1) + MiB(1)`)
   resolves through the bits representation, so the result is
   unit-correct.

4. **Comparison and bitwise.** Comparisons (`<`, `>`, `==`) and
   bitwise operations (`&`, `|`, `^`, `~`, `<<`, `>>`) work on the
   internal bits representation.

5. **Formatting.** `str()`, `repr()`, and `format()` (including
   f-string usage) produce human-readable output. The `best_prefix`
   function picks the most readable unit for a given byte value.

6. **Parsing.** `parse_string` and `parse_string_unsafe` accept a
   string like `"4.5 GiB"` and return a bitmath instance. The strict
   form raises on ambiguous unit; the unsafe form picks a default
   system (SI by default) when the unit is ambiguous.

7. **Filesystem inspection.** `getsize` accepts a path or
   `pathlib.Path` and returns a bitmath instance for the file size.
   `listdir` (deprecated in 2.1.0) walks a tree and yields sizes.

8. **Capacity querying.** `query_capacity(path)` returns a
   `Capacity(total, used, free)` named tuple of `Byte` instances.
   This uses `shutil.disk_usage` and works on every supported
   platform without elevated privileges. `query_device_capacity(fd)`
   returns the raw physical block-device capacity and requires
   elevated privileges on Linux (root) and Windows (administrator);
   macOS raises `NotImplementedError`.

### Data Flow

Untrusted input enters the library at exactly three runtime places:
the string parsers (`parse_string`, `parse_string_unsafe`), the
filesystem helpers (`getsize`, `listdir`), and the capacity functions
(`query_capacity`, `query_device_capacity`). For everything else the
input is a Python number or another bitmath instance, both of which
are inherently trusted. The trust boundaries section below covers
what bitmath does and does not validate at each entry point. See
[SECURITY_ASSESSMENT.md](SECURITY_ASSESSMENT.md) for the full threat
model.

## Build and Release Pipeline

### Component Inventory

| Actor | Lives at | What it does |
|-------|----------|--------------|
| Source repository | github.com/timlnx/bitmath | Single source of truth for all code, docs, and pipeline configuration |
| `VERSION` file | Repository root | Single source of the project version; read by Hatchling and the Makefile |
| `pyproject.toml` | Repository root | PEP 517/518/621 project metadata; declares Hatchling as the build backend |
| Hatchling | Build-time only | PyPA-blessed build backend; produces the wheel and sdist artifacts |
| `Makefile` | Repository root | Local automation; targets like `make ci`, `make build`, `make docs` |
| GitHub Actions runners | `.github/workflows/*.yml` | Hosted CI execution environment |
| `publish.yml` workflow | `.github/workflows/publish.yml` | Two-job workflow: build artifacts, then publish via OIDC |
| PyPI Trusted Publishing | PyPI's OIDC verifier | Validates the OIDC token from the `publish.yml` workflow and authorizes the upload |
| PyPI | pypi.org | The distribution channel; serves wheels and sdists over HTTPS to `pip` |
| Read The Docs | bitmath.readthedocs.io | Hosts the rendered documentation; rebuilds on push to master |

### Pipeline View

```
                  +------------------------+
                  | Developer              |
                  | (see MAINTAINERS.md)   |
                  +-----------+------------+
                              | git push, git tag
                              v
                  +------------------------+
                  | GitHub repository      |
                  |   timlnx/bitmath       |
                  |   branch protection on |
                  |   master (17 required  |
                  |   checks, enforce      |
                  |   admins)              |
                  +-----------+------------+
                              | release: published
                              v
                  +------------------------+
                  | publish.yml workflow   |
                  |                        |
                  | Job 1: build           |
                  |   pip install build    |
                  |   python -m build      |
                  |   -> dist/ artifacts   |
                  |                        |
                  | Job 2: publish         |
                  |   id-token: write      |
                  |   PyPI OIDC exchange   |
                  +-----------+------------+
                              | OIDC-authenticated upload
                              v
                  +------------------------+
                  | PyPI                   |
                  |   pypi.org/project     |
                  |     /bitmath/          |
                  |   wheel + sdist        |
                  |   + PEP 740            |
                  |     attestations       |
                  +-----------+------------+
                              | pip install bitmath
                              v
                  +------------------------+
                  | Consumer's process     |
                  +------------------------+
```

### Actions

1. **Version bump.** I edit `VERSION` to the new SemVer string.
   `pyproject.toml` reads this dynamically via `[tool.hatch.version]`;
   the Makefile reads it for docs and man pages. There is no other
   place to update.

2. **Changelog.** I add the section for the new version to
   `NEWS.rst`.

3. **Tag and push.** A signed tag is pushed to GitHub.

4. **Create a GitHub Release.** Releasing from the tag fires the
   `release: published` event. The `publish.yml` workflow has no
   other trigger; it cannot fire on pull requests or direct pushes.

5. **Build job.** Runs on a clean ubuntu-latest runner with Python
   3.12. Installs `build`, runs `python -m build`, uploads the
   `dist/` directory as a workflow artifact.

6. **Publish job.** Depends on the build job. Downloads the artifact.
   Requests an OIDC token (`id-token: write`) from GitHub Actions and
   exchanges it with PyPI for short-lived upload credentials via
   Trusted Publishing. Uploads the wheel and sdist. No long-lived
   PyPI API token exists anywhere in the project.

7. **Consumer install.** A consumer runs `pip install bitmath`.
   `pip` fetches the wheel over HTTPS from PyPI, verifies the package
   against the published SHA-256 hash, and installs into their
   environment.

## CI and Quality Gates

CI runs continuously on `master` and on every pull request. These
actors influence what is merged but do not produce released
artifacts. They are summarized here for completeness; the source of
truth for each is the corresponding workflow file in
`.github/workflows/`.

| Actor | Workflow | What it gates |
|-------|----------|---------------|
| pytest matrix | `python.yml` | Full test suite across Python 3.9–3.13 on macOS, Ubuntu, Windows |
| Bandit | `bandit.yml` | Python security smell analysis across `bitmath/` and `tests/` |
| CodeQL | `codeql.yml` | Semantic analysis for Python vulnerabilities |
| OSSF Scorecard | `scorecard.yml` | Weekly repository security posture report |
| Dependabot | `.github/dependabot.yml` | Automated dependency update pull requests |

The first three are required status checks on the `master` branch.
Merges are blocked until they pass. `enforce_admins: true` so I
cannot bypass them.

## Trust Boundaries

bitmath validates input only at the places untrusted data enters the
library. The ingress points are:

* **String parsing** (`parse_string`, `parse_string_unsafe`).
  Regex-driven, no `eval`, raises `ValueError` on anything
  malformed. Hypothesis-based fuzzing tests exercise this path.
* **Filesystem paths** (`getsize`, `listdir`). bitmath does no path
  sanitization. The consumer is responsible for validating paths
  before passing them in. This is documented behavior; sanitization
  rules depend on the consumer's threat model in ways the library
  cannot anticipate.
* **File descriptors** (`query_device_capacity`). Operates only on
  descriptors the consumer already opened. The ioctl arguments are
  fixed constants; no untrusted input flows into the kernel call.
* **The build pipeline.** `publish.yml` cannot be triggered by a
  pull request, only by a release event. Untrusted contributor code
  never touches PyPI credentials. Branch protection prevents direct
  pushes to master from bypassing CI.

See [SECURITY_ASSESSMENT.md](SECURITY_ASSESSMENT.md) for the full
threat model and the specific mitigations at each boundary.

## Documentation Pipeline

The documentation lives in `docsite/source/`. Sphinx builds it.
`index.rst.in` is the source template; `index.rst` is generated from
`index.rst.in` plus `README.rst` by `make docs`. Editing `index.rst`
directly is wrong because the next `make docs` will overwrite it.

Read The Docs runs the same build automatically on push to master
and publishes the result at https://bitmath.readthedocs.io/.

## Maintenance

This document is reviewed at every minor release. The contract:

* New public API → update the Runtime architecture component
  inventory and the actions list.
* New CI workflow or build pipeline change → update Build and
  release pipeline and/or CI and quality gates.
* New trust boundary → update Trust boundaries here and the threat
  model in [SECURITY_ASSESSMENT.md](SECURITY_ASSESSMENT.md).
* Build-backend or package-tooling change → update Build and release
  pipeline.

If this document drifts out of date, that is a defect worth
[opening an issue](https://github.com/timlnx/bitmath/issues/new) or
a PR.
