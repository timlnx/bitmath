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
Tests for parse_string (strict=True, the default) and public entry-point behaviour.
"""

import warnings

from . import TestCase
import bitmath


class TestParseStrict(TestCase):
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

    def test_parse_Zio(self):
        """parse_string works on zebioctet strings"""
        self.assertEqual(
            bitmath.parse_string("654 Zio"),
            bitmath.ZiB(654))

    def test_parse_Yio(self):
        """parse_string works on yobioctet strings"""
        self.assertEqual(
            bitmath.parse_string("654 Yio"),
            bitmath.YiB(654))

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

    def test_parse_Zo(self):
        """parse_string works on zettaoctet strings"""
        self.assertEqual(
            bitmath.parse_string("654 Zo"),
            bitmath.ZB(654))

    def test_parse_Yo(self):
        """parse_string works on yottaoctet strings"""
        self.assertEqual(
            bitmath.parse_string("654 Yo"),
            bitmath.YB(654))

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
    # Deprecated public entry point tests

    def test_parse_string_unsafe_deprecation_warning(self):
        """parse_string_unsafe emits DeprecationWarning as of 2.0.0"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            bitmath.parse_string_unsafe("100 GiB")
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("2.0.0", str(w[0].message))
            self.assertIn("parse_string", str(w[0].message))

    def test_parse_string_unsafe_request_NIST(self):
        """parse_string_unsafe still delegates correctly with explicit system"""
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
