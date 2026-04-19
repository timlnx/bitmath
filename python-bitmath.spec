Name:           python-bitmath
Summary:        Work with file sizes like numbers — convert, compare, sort, and format across any unit prefix
Version:        0
Release:        1%{?dist}
License:        MIT
Source0:        https://github.com/timlnx/bitmath/archive/refs/tags/v%{version}.tar.gz
URL:            https://github.com/timlnx/bitmath

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-hatchling
BuildRequires:  python3-pytest

%description
bitmath simplifies many facets of interacting with file sizes in
various units. Examples include: converting between SI and NIST prefix
units (GiB to kB), converting between units of the same type (SI to
SI, or NIST to NIST), basic arithmetic operations (subtracting 42KiB
from 50GiB), and rich comparison operations (1024 Bytes == 1KiB),
bit-wise operations, sorting, automatic best human-readable prefix
selection, and completely customizable formatting.

In addition to the conversion and math operations, bitmath provides
human readable representations of values which are suitable for use in
interactive shells as well as larger scripts and applications. It can
also read the capacity of system storage devices. bitmath can parse
strings (like "1 KiB") into proper objects and has support for
integration with the argparse module as a custom argument type.

bitmath ships almost 300 unit tests with near 100% code coverage.

######################################################################
# Sub-package setup
%package -n python3-bitmath
Summary:        Aids representing and manipulating file sizes in various prefix notations

%description -n python3-bitmath
bitmath simplifies many facets of interacting with file sizes in
various units. Examples include: converting between SI and NIST prefix
units (GiB to kB), converting between units of the same type (SI to
SI, or NIST to NIST), basic arithmetic operations (subtracting 42KiB
from 50GiB), and rich comparison operations (1024 Bytes == 1KiB),
bit-wise operations, sorting, automatic best human-readable prefix
selection, and completely customizable formatting.

In addition to the conversion and math operations, bitmath provides
human readable representations of values which are suitable for use in
interactive shells as well as larger scripts and applications. It can
also read the capacity of system storage devices. bitmath can parse
strings (like "1 KiB") into proper objects and has support for
integration with the argparse module as a custom argument type.

bitmath ships almost 300 unit tests with near 100% code coverage.

######################################################################
%generate_buildrequires
%pyproject_buildrequires

######################################################################
%prep
%setup -n bitmath-%{version} -q

######################################################################
%build
%pyproject_wheel

######################################################################
%install
%pyproject_install
%pyproject_save_files bitmath
pushd %{buildroot}%{_bindir}
ln -s bitmath bitmath-%{python3_version}
popd
mkdir -p %{buildroot}%{_mandir}/man1/
cp -v *.1 %{buildroot}%{_mandir}/man1/
ln -s bitmath.1 %{buildroot}%{_mandir}/man1/bitmath-%{python3_version}.1
mkdir -p %{buildroot}%{_docdir}/%{name}/docs
cp -v -r docsite/source/* %{buildroot}%{_docdir}/%{name}/docs/
find %{buildroot}%{_docdir}/%{name}/docs -name '.gitkeep' -delete

######################################################################
%check
%pytest tests/

######################################################################
%files
%license LICENSE

######################################################################
%files -n python3-bitmath -f %{pyproject_files}
%license LICENSE
%doc README.rst NEWS.rst
%{_bindir}/bitmath
%{_bindir}/bitmath-%{python3_version}
%{_mandir}/man1/bitmath.1*
%{_mandir}/man1/bitmath-%{python3_version}.1*
%{_docdir}/%{name}/

######################################################################
%changelog
* Sat Apr 18 2026 Tim Case <bitmath@lnx.cx> - 0-1
- Packit-managed changelog. See https://github.com/timlnx/bitmath/releases
