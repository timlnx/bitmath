# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# The MIT License (MIT)
#
# Copyright © 2014 Tim Case <timbielawa@gmail.com>
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
Test parsing strings into bitmath objects
"""

from . import TestCase
import bitmath


class TestParse(TestCase):
    def test_parse_b(self):
        """parse_string works on bit strings"""
        self.assertEqual(
            bitmath.parse_string("123b"),
            bitmath.Bit(123))

    def test_parse_B(self):
        """parse_string works on byte strings"""
        self.assertEqual(
            bitmath.parse_string("321B"),
            bitmath.Byte(321))

    def test_parse_Gb(self):
        """parse_string works on gigabit strings"""
        self.assertEqual(
            bitmath.parse_string("456Gb"),
            bitmath.Gb(456))

    def test_parse_MiB(self):
        """parse_string works on mebibyte strings"""
        self.assertEqual(
            bitmath.parse_string("654 MiB"),
            bitmath.MiB(654))

    ######################################################################
    # NIST 'octet' based units
    def test_parse_Mio(self):
        """parse_string works on mebioctet strings"""
        self.assertEqual(
            bitmath.parse_string("654 Mio"),
            bitmath.MiB(654))

    def test_parse_Eio(self):
        """parse_string works on exbioctet strings"""
        self.assertEqual(
            bitmath.parse_string("654 Eio"),
            bitmath.EiB(654))

    # SI 'octet' based units
    def test_parse_Mo(self):
        """parse_string works on megaoctet strings"""
        self.assertEqual(
            bitmath.parse_string("654 Mo"),
            bitmath.MB(654))

    def test_parse_Eo(self):
        """parse_string works on exaoctet strings"""
        self.assertEqual(
            bitmath.parse_string("654 Eo"),
            bitmath.EB(654))

    ######################################################################

    def test_parse_bad_float(self):
        """parse_string can identify invalid float values"""
        with self.assertRaises(ValueError):
            bitmath.parse_string("1.23.45 kb")

    def test_parse_bad_unit(self):
        """parse_string can identify invalid prefix units"""
        with self.assertRaises(ValueError):
            bitmath.parse_string("1.23 GIB")

    def test_parse_bad_unit2(self):
        """parse_string can identify other prefix units"""
        with self.assertRaises(ValueError):
            bitmath.parse_string("1.23 QB")

    def test_parse_no_unit(self):
        """parse_string can identify strings without units at all"""
        with self.assertRaises(ValueError):
            bitmath.parse_string("12345")

    def test_parse_string_non_string_input(self):
        """parse_string can identify a non-string input"""
        with self.assertRaises(ValueError):
            bitmath.parse_string(12345)

    def test_parse_string_unicode(self):
        """parse_string can handle a unicode string"""
        self.assertEqual(
            bitmath.parse_string(u"750 GiB"),
            bitmath.GiB(750))

    ######################################################################

    def test_parse_loose_bad_input_type(self):
        """parse_string strict=False can identify invalid input types"""
        with self.assertRaises(ValueError):
            bitmath.parse_string({'keyvalue': 'store'}, strict=False)

    def test_parse_loose_invalid_input(self):
        """parse_string strict=False raises ValueError for invalid units"""
        with self.assertRaises(ValueError):
            bitmath.parse_string("kitties!", strict=False)

        with self.assertRaises(ValueError):
            bitmath.parse_string('100 CiB', strict=False)

        with self.assertRaises(ValueError):
            bitmath.parse_string('100 J', strict=False)

    def test_parse_loose_good_number_input(self):
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

    def test_parse_loose_handles_SI_K_unit(self):
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

    def test_parse_loose_NIST_units(self):
        """parse_string strict=False can parse abbreviated NIST units (Gi, Ki, ...)"""
        nist_input = "100 Gi"
        expected_result = bitmath.GiB(100)

        self.assertEqual(
            bitmath.parse_string(nist_input, strict=False),
            expected_result)

    def test_parse_loose_SI(self):
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

    def test_parse_loose_NIST(self):
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

    def test_parse_loose_default_system_is_NIST(self):
        """parse_string strict=False defaults to NIST for ambiguous single-letter units"""
        self.assertEqual(
            bitmath.parse_string("100M", strict=False),
            bitmath.MiB(100))
        self.assertIs(
            type(bitmath.parse_string("100k", strict=False)),
            bitmath.KiB)

    def test_parse_loose_explicit_SI(self):
        """parse_string strict=False uses SI when system=bitmath.SI"""
        self.assertEqual(
            bitmath.parse_string("100M", strict=False, system=bitmath.SI),
            bitmath.MB(100))
        self.assertIs(
            type(bitmath.parse_string("100k", strict=False, system=bitmath.SI)),
            bitmath.kB)

    def test_parse_loose_number_inputs_unaffected_by_system(self):
        """parse_string strict=False returns Byte() for plain numbers regardless of system"""
        self.assertEqual(
            bitmath.parse_string("100", strict=False, system=bitmath.NIST),
            bitmath.Byte(100))
        self.assertEqual(
            bitmath.parse_string(100, strict=False, system=bitmath.SI),
            bitmath.Byte(100))

    def test_parse_loose_github_issue_60(self):
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

    def test_parse_string_unsafe_deprecation_warning(self):
        """parse_string_unsafe emits DeprecationWarning as of 2.0.0"""
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            bitmath.parse_string_unsafe("100 GiB")
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("2.0.0", str(w[0].message))
            self.assertIn("parse_string", str(w[0].message))

    def test_parse_string_unsafe_request_NIST(self):
        """parse_string_unsafe still delegates correctly with explicit system"""
        import warnings
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")

            _parsed = bitmath.parse_string_unsafe("100M", system=bitmath.NIST)
            self.assertEqual(_parsed, bitmath.MiB(100))
            self.assertIs(type(_parsed), bitmath.MiB)

            _parsed2 = bitmath.parse_string_unsafe("100k", system=bitmath.NIST)
            self.assertEqual(_parsed2, bitmath.KiB(100))
            self.assertIs(type(_parsed2), bitmath.KiB)

            _parsed3 = bitmath.parse_string_unsafe("100", system=bitmath.NIST)
            self.assertEqual(_parsed3, bitmath.Byte(100))
            self.assertIs(type(_parsed3), bitmath.Byte)

            _parsed4 = bitmath.parse_string_unsafe("100kb", system=bitmath.NIST)
            self.assertEqual(_parsed4, bitmath.KiB(100))
            self.assertIs(type(_parsed4), bitmath.KiB)
