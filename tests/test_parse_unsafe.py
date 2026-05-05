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
Tests for parse_string with strict=False (the non-strict / formerly unsafe path).
"""

from . import TestCase
import bitmath


class TestParseUnsafe(TestCase):
    def test_parse_non_strict_bad_input_type(self):
        """parse_string strict=False can identify invalid input types"""
        with self.assertRaises(ValueError):
            bitmath.parse_string({'keyvalue': 'store'}, strict=False)

    def test_parse_non_strict_invalid_input(self):
        """parse_string strict=False raises ValueError for invalid units"""
        with self.assertRaises(ValueError):
            bitmath.parse_string("kitties!", strict=False)

        with self.assertRaises(ValueError):
            bitmath.parse_string('100 CiB', strict=False)

        with self.assertRaises(ValueError):
            bitmath.parse_string('100 J', strict=False)

    def test_parse_non_strict_good_number_input(self):
        """parse_string strict=False can parse unitless number inputs"""
        number_input = 100
        string_input = "100"
        expected_result = bitmath.Byte(100)

        self.assertEqual(
            bitmath.parse_string(number_input, strict=False),
            expected_result)
        self.assertEqual(
            bitmath.parse_string(string_input, strict=False),
            expected_result)

    def test_parse_non_strict_handles_SI_K_unit(self):
        """parse_string strict=False can parse the upper/lowercase SI 'thousand' (k)"""
        thousand_lower = "100k"
        thousand_upper = "100K"
        expected_result = bitmath.kB(100)

        self.assertEqual(
            bitmath.parse_string(thousand_lower, strict=False, system=bitmath.SI),
            expected_result)
        self.assertEqual(
            bitmath.parse_string(thousand_upper, strict=False, system=bitmath.SI),
            expected_result)

    def test_parse_non_strict_NIST_units(self):
        """parse_string strict=False can parse abbreviated NIST units (Gi, Ki, ...)"""
        nist_input = "100 Gi"
        expected_result = bitmath.GiB(100)

        self.assertEqual(
            bitmath.parse_string(nist_input, strict=False),
            expected_result)

    def test_parse_non_strict_SI(self):
        """parse_string strict=False can parse all accepted SI inputs"""
        kilo_inputs = [
            '100k',
            '100K',
            '100kb',
            '100KB',
            '100kB'
        ]
        expected_kilo_result = bitmath.kB(100)

        for ki in kilo_inputs:
            _parsed = bitmath.parse_string(ki, strict=False, system=bitmath.SI)
            self.assertEqual(_parsed, expected_kilo_result)
            self.assertIs(type(_parsed), type(expected_kilo_result))

        other_inputs = [
            '100g',
            '100G',
            '100gb',
            '100gB',
            '100GB'
        ]
        expected_gig_result = bitmath.GB(100)

        for gi in other_inputs:
            _parsed = bitmath.parse_string(gi, strict=False, system=bitmath.SI)
            self.assertEqual(_parsed, expected_gig_result)
            self.assertIs(type(_parsed), type(expected_gig_result))

    def test_parse_non_strict_NIST(self):
        """parse_string strict=False can parse all accepted NIST inputs"""
        kilo_inputs = [
            '100ki',
            '100Ki',
            '100kib',
            '100KiB',
            '100kiB'
        ]
        expected_kilo_result = bitmath.KiB(100)

        for ki in kilo_inputs:
            _parsed = bitmath.parse_string(ki, strict=False)
            self.assertEqual(_parsed, expected_kilo_result)
            self.assertIs(type(_parsed), type(expected_kilo_result))

        other_inputs = [
            '100gi',
            '100Gi',
            '100gib',
            '100giB',
            '100GiB'
        ]
        expected_gig_result = bitmath.GiB(100)

        for gi in other_inputs:
            _parsed = bitmath.parse_string(gi, strict=False)
            self.assertEqual(_parsed, expected_gig_result)
            self.assertIs(type(_parsed), type(expected_gig_result))

    def test_parse_non_strict_default_system_is_NIST(self):
        """parse_string strict=False defaults to NIST for ambiguous single-letter units"""
        self.assertEqual(
            bitmath.parse_string("100M", strict=False),
            bitmath.MiB(100))
        self.assertIs(
            type(bitmath.parse_string("100k", strict=False)),
            bitmath.KiB)

    def test_parse_non_strict_explicit_SI(self):
        """parse_string strict=False uses SI when system=bitmath.SI"""
        self.assertEqual(
            bitmath.parse_string("100M", strict=False, system=bitmath.SI),
            bitmath.MB(100))
        self.assertIs(
            type(bitmath.parse_string("100k", strict=False, system=bitmath.SI)),
            bitmath.kB)

    def test_parse_non_strict_number_inputs_unaffected_by_system(self):
        """parse_string strict=False returns Byte() for plain numbers regardless of system"""
        self.assertEqual(
            bitmath.parse_string("100", strict=False, system=bitmath.NIST),
            bitmath.Byte(100))
        self.assertEqual(
            bitmath.parse_string(100, strict=False, system=bitmath.SI),
            bitmath.Byte(100))

    def test_parse_non_strict_github_issue_60(self):
        """parse_string strict=False can parse the examples reported in issue #60

https://github.com/timlnx/bitmath/issues/60
        """
        self.assertEqual(
            bitmath.parse_string('7.5KB', strict=False, system=bitmath.SI),
            bitmath.kB(7.5))

        self.assertEqual(
            bitmath.parse_string('4.7MB', strict=False, system=bitmath.SI),
            bitmath.MB(4.7))

        self.assertEqual(
            bitmath.parse_string('4.7M', strict=False, system=bitmath.SI),
            bitmath.MB(4.7))

    def test_parse_non_strict_capital_B_is_Byte(self):
        """parse_string strict=False: lone 'B' parses as Byte"""
        self.assertIs(type(bitmath.parse_string("1B", strict=False)), bitmath.Byte)
        self.assertEqual(bitmath.parse_string("1 B", strict=False), bitmath.Byte(1))

    def test_parse_non_strict_lowercase_b_is_Bit(self):
        """parse_string strict=False: lone 'b' parses as Bit"""
        self.assertIs(type(bitmath.parse_string("1b", strict=False)), bitmath.Bit)
        self.assertEqual(bitmath.parse_string("1 b", strict=False), bitmath.Bit(1))

    def test_parse_non_strict_bit_word_forms(self):
        """parse_string strict=False: bit/bits/Bit/Bits/BIT all parse as Bit"""
        expected = bitmath.Bit(42)
        for unit in ('bit', 'bits', 'Bit', 'Bits', 'BIT', 'BITS'):
            result = bitmath.parse_string(f"42 {unit}", strict=False)
            self.assertEqual(result, expected, msg=f"Failed for unit '{unit}'")
            self.assertIs(type(result), bitmath.Bit, msg=f"Wrong type for unit '{unit}'")

    def test_parse_non_strict_byte_word_forms(self):
        """parse_string strict=False: byte/bytes/Byte/Bytes/BYTE all parse as Byte"""
        expected = bitmath.Byte(42)
        for unit in ('byte', 'bytes', 'Byte', 'Bytes', 'BYTE', 'BYTES'):
            result = bitmath.parse_string(f"42 {unit}", strict=False)
            self.assertEqual(result, expected, msg=f"Failed for unit '{unit}'")
            self.assertIs(type(result), bitmath.Byte, msg=f"Wrong type for unit '{unit}'")
