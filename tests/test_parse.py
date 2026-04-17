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

    def test_parse_unsafe_bad_input_type(self):
        """parse_string_unsafe can identify invalid input types"""
        with self.assertRaises(ValueError):
            invalid_input = {'keyvalue': 'store'}
            bitmath.parse_string_unsafe(invalid_input)

    def test_parse_unsafe_invalid_input(self):
        """parse_string_unsafe explodes when given invalid units"""
        invalid_input_str = "kitties!"
        with self.assertRaises(ValueError):
            bitmath.parse_string_unsafe(invalid_input_str)

        with self.assertRaises(ValueError):
            bitmath.parse_string_unsafe('100 CiB')

        with self.assertRaises(ValueError):
            bitmath.parse_string_unsafe('100 J')

    def test_parse_unsafe_good_number_input(self):
        """parse_string_unsafe can parse unitless number inputs"""
        number_input = 100
        string_input = "100"
        expected_result = bitmath.Byte(100)

        self.assertEqual(
            bitmath.parse_string_unsafe(number_input),
            expected_result)
        self.assertEqual(
            bitmath.parse_string_unsafe(string_input),
            expected_result)

    def test_parse_unsafe_handles_SI_K_unit(self):
        """parse_string_unsafe can parse the upper/lowercase SI 'thousand' (k)"""
        thousand_lower = "100k"
        thousand_upper = "100K"
        expected_result = bitmath.kB(100)

        self.assertEqual(
            bitmath.parse_string_unsafe(thousand_lower),
            expected_result)
        self.assertEqual(
            bitmath.parse_string_unsafe(thousand_upper),
            expected_result)

    def test_parse_unsafe_NIST_units(self):
        """parse_string_unsafe can parse abbreviated NIST units (Gi, Ki, ...)"""
        nist_input = "100 Gi"
        expected_result = bitmath.GiB(100)

        self.assertEqual(
            bitmath.parse_string_unsafe(nist_input),
            expected_result)

    def test_parse_unsafe_SI(self):
        """parse_string_unsafe can parse all accepted SI inputs"""
        # Begin with the kilo unit because it's the most tricky (SI
        # defines the unit as a lower-case 'k')
        kilo_inputs = [
            '100k',
            '100K',
            '100kb',
            '100KB',
            '100kB'
        ]
        expected_kilo_result = bitmath.kB(100)

        for ki in kilo_inputs:
            _parsed = bitmath.parse_string_unsafe(ki)
            self.assertEqual(_parsed, expected_kilo_result)
            self.assertIs(type(_parsed), type(expected_kilo_result))

        # Now check for other easier to parse prefixes
        other_inputs = [
            '100g',
            '100G',
            '100gb',
            '100gB',
            '100GB'
        ]

        expected_gig_result = bitmath.GB(100)

        for gi in other_inputs:
            _parsed = bitmath.parse_string_unsafe(gi)
            self.assertEqual(_parsed, expected_gig_result)
            self.assertIs(type(_parsed), type(expected_gig_result))

    def test_parse_unsafe_NIST(self):
        """parse_string_unsafe can parse all accepted NIST inputs"""
        # Begin with the kilo unit because it's the most tricky (SI
        # defines the unit as a lower-case 'k')
        kilo_inputs = [
            '100ki',
            '100Ki',
            '100kib',
            '100KiB',
            '100kiB'
        ]
        expected_kilo_result = bitmath.KiB(100)

        for ki in kilo_inputs:
            _parsed = bitmath.parse_string_unsafe(ki)
            self.assertEqual(_parsed, expected_kilo_result)
            self.assertIs(type(_parsed), type(expected_kilo_result))

        # Now check for other easier to parse prefixes
        other_inputs = [
            '100gi',
            '100Gi',
            '100gib',
            '100giB',
            '100GiB'
        ]

        expected_gig_result = bitmath.GiB(100)

        for gi in other_inputs:
            _parsed = bitmath.parse_string_unsafe(gi)
            self.assertEqual(_parsed, expected_gig_result)
            self.assertIs(type(_parsed), type(expected_gig_result))

    def test_parse_string_unsafe_request_NIST(self):
        """parse_string_unsafe can convert to NIST on request"""
        unsafe_input = "100M"
        _parsed = bitmath.parse_string_unsafe(unsafe_input, system=bitmath.NIST)
        expected = bitmath.MiB(100)

        self.assertEqual(_parsed, expected)
        self.assertIs(type(_parsed), type(expected))

        unsafe_input2 = "100k"
        _parsed2 = bitmath.parse_string_unsafe(unsafe_input2, system=bitmath.NIST)
        expected2 = bitmath.KiB(100)

        self.assertEqual(_parsed2, expected2)
        self.assertIs(type(_parsed2), type(expected2))

        unsafe_input3 = "100"
        _parsed3 = bitmath.parse_string_unsafe(unsafe_input3, system=bitmath.NIST)
        expected3 = bitmath.Byte(100)

        self.assertEqual(_parsed3, expected3)
        self.assertIs(type(_parsed3), type(expected3))

        unsafe_input4 = "100kb"
        _parsed4 = bitmath.parse_string_unsafe(unsafe_input4, system=bitmath.NIST)
        expected4 = bitmath.KiB(100)

        self.assertEqual(_parsed4, expected4)
        self.assertIs(type(_parsed4), type(expected4))

    ######################################################################

    def test_parse_string_unsafe_github_issue_60(self):
        """parse_string_unsafe can parse the examples reported in issue #60

https://github.com/timlnx/bitmath/issues/60
        """
        issue_input1 = '7.5KB'
        _parsed1 = bitmath.parse_string_unsafe(issue_input1)
        expected_result1 = bitmath.kB(7.5)

        self.assertEqual(
            _parsed1,
            expected_result1)

        issue_input2 = '4.7MB'
        _parsed2 = bitmath.parse_string_unsafe(issue_input2)
        expected_result2 = bitmath.MB(4.7)

        self.assertEqual(
            _parsed2,
            expected_result2)

        issue_input3 = '4.7M'
        _parsed3 = bitmath.parse_string_unsafe(issue_input3)
        expected_result3 = bitmath.MB(4.7)

        self.assertEqual(
            _parsed3,
            expected_result3)
