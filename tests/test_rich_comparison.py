# -*- coding: utf-8 -*-
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
Test for rich comparison operations: LT, LE, EQ, NE, GT, GE
"""

from . import TestCase
import bitmath


class TestRichComparison(TestCase):
    def setUp(self):
        self.kib = bitmath.KiB(1)
        self.mib = bitmath.MiB(1)
        self.gib = bitmath.GiB(1)

    ##################################################################
    # Test bitmath comparisons
    def test_less_than(self):
        """One KiB is less than one MiB"""
        self.assertLess(self.kib, self.mib)

    def test_less_than_equal(self):
        """Smaller or equal is less than or equal to one MiB"""
        # True - 1 KiB is less than 1 MiB
        self.assertLessEqual(self.kib, self.mib)
        # True - 1024 KiB is equal to 1 MiB
        self.assertLessEqual(bitmath.KiB(1024), self.mib)

    def test_greater_than(self):
        """1 GiB is greater than 1 Mib"""
        self.assertGreater(self.gib, self.mib)

    def test_greater_than_equal(self):
        """Greater or equal is more than or equal to one MiB"""
        # True - 1 GiB is greater than 1 MiB
        self.assertGreaterEqual(self.gib, self.mib)
        # True - 1024 KiB is equal to 1 MiB
        self.assertGreaterEqual(self.mib, bitmath.GiB(1 / 1024.0))

    ##################################################################
    # Same tests, but against numbers instead of bitmaths
    def test_less_than_num(self):
        """One KiB is less than int(2)"""
        self.assertLess(self.kib, 2)

    def test_less_than_equal_num(self):
        """Smaller or equal is less than or equal to int(2)"""
        # True - 1 KiB is less than 2
        self.assertLessEqual(self.kib, 2)
        # True - 1024 KiB is equal to 1024
        self.assertLessEqual(bitmath.KiB(1024), 1024)

    def test_greater_than_num(self):
        """1 GiB is greater than 0.5"""
        self.assertGreater(self.gib, 0.5)

    def test_greater_than_equal_num(self):
        """Greater or equal is more than or equal to int(1)"""
        # True - 1 GiB is equal to 1
        self.assertGreaterEqual(self.gib, 1)
        # True - 1024 KiB is greater than 0.5
        self.assertGreaterEqual(self.mib, 0.5)

    ##################################################################
    # Equality testing
    def test_equal(self):
        """Two equal values are actually equal"""
        self.assertEqual(self.mib, bitmath.KiB(1024))

    def test_equal_false(self):
        """Unequal objects aren't equal"""
        self.assertNotEqual(self.kib, self.gib)

    ##################################################################
    # Equality testing against numbers
    def test_equal_num(self):
        """Two equal values are actually equal with numbers"""
        self.assertEqual(self.mib, 1)

    def test_equal_false_num(self):
        """Unequal objects aren't equal with numbers"""
        self.assertNotEqual(self.kib, 42)
