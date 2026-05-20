# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# The MIT License (MIT)
#
# SPDX-FileCopyrightText: 2014-2026 Tim Case <bitmath@lnx.cx>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Hypothesis-driven property tests for the bitmath parser and unit
conversions. These are fuzz-style tests: hypothesis generates inputs
across the value/unit space and shrinks any counterexample it finds.

Three invariants are checked:

1. Roundtrip: an instance formatted as "value unit_singular" and then
   re-parsed produces a Bitmath with the same underlying bit count.
2. Lossless conversion: x.to_DST().to_SRC() preserves x.bits across
   every (SRC, DST) pair in ALL_UNIT_TYPES.
3. Parser exception contract: parse_string raises only ValueError on
   bad input. A leaked IndexError, AttributeError, KeyError, or
   TypeError would be a bug.
"""

import math

import pytest

# Downstream packagers (Fedora/EPEL RPM builds) run %check without
# installing test-only dependencies. Skip the whole module when
# hypothesis isn't on the path rather than failing collection.
pytest.importorskip("hypothesis")

from hypothesis import given, settings, strategies as st  # noqa: E402

import bitmath  # noqa: E402


# Bracketed to avoid values that Python's str() renders in scientific
# notation. The parser splits a value/unit string on the first
# alphabetic character, which mis-handles the 'e' in '1e+16' or
# '1e-05'. Scientific-notation file sizes aren't a realistic user
# input, so the test space stays in the regular-notation range
# (approximately [1e-4, 1e16)), plus exactly zero.
nonneg_finite = st.one_of(
    st.just(0.0),
    st.floats(
        min_value=1e-4,
        max_value=1e15,
        allow_nan=False,
        allow_infinity=False,
    ),
)

unit_names = list(bitmath.ALL_UNIT_TYPES)


@given(value=nonneg_finite, unit=st.sampled_from(unit_names))
@settings(max_examples=200)
def test_parse_string_roundtrip(value, unit):
    cls = getattr(bitmath, unit)
    original = cls(value)
    formatted = original.format("{value} {unit_singular}")
    parsed = bitmath.parse_string(formatted)
    assert math.isclose(parsed.bits, original.bits, rel_tol=1e-9, abs_tol=1e-9)


@given(
    value=nonneg_finite,
    src=st.sampled_from(unit_names),
    dst=st.sampled_from(unit_names),
)
@settings(max_examples=300)
def test_unit_conversion_lossless(value, src, dst):
    src_cls = getattr(bitmath, src)
    original = src_cls(value)
    via = getattr(original, f"to_{dst}")()
    back = getattr(via, f"to_{src}")()
    assert math.isclose(back.bits, original.bits, rel_tol=1e-9, abs_tol=1e-9)


@given(garbage=st.text())
@settings(max_examples=500)
def test_parse_string_strict_only_raises_value_error(garbage):
    try:
        result = bitmath.parse_string(garbage)
    except ValueError:
        return
    assert isinstance(result, bitmath.Bitmath)


@given(garbage=st.text())
@settings(max_examples=500)
def test_parse_string_unsafe_only_raises_value_error(garbage):
    try:
        result = bitmath.parse_string(garbage, strict=False)
    except ValueError:
        return
    assert isinstance(result, bitmath.Bitmath)
