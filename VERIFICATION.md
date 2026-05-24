# Verifying a bitmath Release

This document explains how to verify that a bitmath release was built
by this project and not tampered with in transit or at rest. It is
aimed at downstream consumers who need to demonstrate due diligence
(organizations subject to the EU Cyber Resilience Act, NIST SSDF, or
similar frameworks) and at anyone who just wants to understand what
guarantees the release process actually provides.

The release pipeline that produces these artifacts is documented in
[ARCHITECTURE.md](ARCHITECTURE.md). The threat model that motivates
this verification stack is in
[SECURITY_ASSESSMENT.md](SECURITY_ASSESSMENT.md).

## What You Can Verify

For every bitmath release on PyPI, three independent properties are
verifiable without trusting the maintainer:

1. **Integrity.** Each wheel and sdist has a published SHA-256 hash.
   `pip` checks this automatically on install. The hash is also
   visible on each file's page on PyPI.
2. **Authenticity.** Each release is built and published by the
   `publish.yml` workflow in `timlnx/bitmath` on GitHub, using
   GitHub Actions OIDC and PyPI Trusted Publishing. The proof of
   that binding is a [PEP 740](https://peps.python.org/pep-0740/)
   attestation attached to each release file.
3. **Provenance.** A CycloneDX Software Bill of Materials (SBOM) is
   attached to each GitHub Release, describing the runtime
   dependency closure of the wheel. bitmath has zero runtime
   dependencies, so this SBOM is short by design.

## Verifying Integrity

`pip` verifies the SHA-256 hash on install. There is normally
nothing you have to do beyond `pip install bitmath`. If you want to
verify a downloaded artifact manually:

```bash
# Get the expected hash from PyPI for, say, version 2.0.1
curl -s https://pypi.org/pypi/bitmath/2.0.1/json \
  | jq -r '.urls[] | "\(.digests.sha256)  \(.filename)"'

# Compute the local hash and compare
shasum -a 256 bitmath-2.0.1-py3-none-any.whl
```

The hashes must match. If they do not, do not install the file.

## Verifying Authenticity (PEP 740 Attestation)

PyPI exposes attestations under each release file's API metadata.
The simplest way to verify them is with the
[pypi-attestations](https://pypi.org/project/pypi-attestations/)
CLI:

```bash
pipx install pypi-attestations

# Download the wheel you want to verify
pip download bitmath==2.0.1 --no-deps -d /tmp/verify-bitmath/

# Verify the attestation
pypi-attestations verify pypi \
  --repository timlnx/bitmath \
  /tmp/verify-bitmath/bitmath-2.0.1-py3-none-any.whl
```

The expected attestation identity is:

* **Source repository**: `timlnx/bitmath`
* **Workflow path**: `.github/workflows/publish.yml`
* **Workflow ref**: `refs/tags/<version>` (the git tag for the
  release)

If verification succeeds, the file was built by GitHub Actions on
`timlnx/bitmath` from a workflow file whose contents you can audit
in the repository at the corresponding tag. The whole signing path
uses [Sigstore](https://www.sigstore.dev/) under the hood. No
long-lived signing keys are involved.

If verification fails, **do not install the file**. Treat it as a
potential supply chain compromise and reach out via the channels in
[SECURITY.md](SECURITY.md).

## Verifying the SBOM

A CycloneDX SBOM is attached to each GitHub Release as
`bitmath-<version>.cdx.json`. Fetch it directly from the release
page:

```bash
curl -L -o bitmath-2.0.1.cdx.json \
  https://github.com/timlnx/bitmath/releases/download/v2.0.1/bitmath-2.0.1.cdx.json
```

You can validate it with any CycloneDX-aware tool. For example, with
[cyclonedx-cli](https://github.com/CycloneDX/cyclonedx-cli):

```bash
cyclonedx validate --input-file bitmath-2.0.1.cdx.json
```

For bitmath, the SBOM should show one primary component (bitmath
itself) plus the small set of components present in the install
environment. The runtime dependency list under bitmath should be
empty, because bitmath has no runtime dependencies by design. If the
SBOM shows additional runtime dependencies under bitmath itself,
that is a defect worth [opening an
issue](https://github.com/timlnx/bitmath/issues/new) about.

## Why This Matters

These verification steps let you confirm three things without
trusting me personally:

* The bytes you have are the bytes PyPI published. (Hash
  verification.)
* The bytes PyPI published came from this repository's release
  workflow. (PEP 740 attestation verification.)
* The dependency surface is what the project claims it is. (SBOM
  verification.)

A compromise that bypasses all three would require simultaneously
breaking the GitHub Actions OIDC infrastructure, the Sigstore
signing chain, and PyPI's storage. That is the threat model the
verification stack is designed against. More plausible compromises
(a stolen API token, a phishing-compromised maintainer account, a
tampered wheel in transit, a malicious dependency injection) are
caught by one or more of these checks.

## Last Review

This document is reviewed at every minor release alongside
[SECURITY_ASSESSMENT.md](SECURITY_ASSESSMENT.md),
[ARCHITECTURE.md](ARCHITECTURE.md), and
[SECURITY_POLICIES.md](SECURITY_POLICIES.md).
