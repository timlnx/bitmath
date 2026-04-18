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
Test for bitwise operations: <<, >>, &, ^, |
"""

from . import TestCase
import bitmath


class TestBitwiseOperations(TestCase):
    def setUp(self):
        self.leet = bitmath.Bit(1337)

    def test_left_shift(self):
        """Bits left shifted (<<) are increased"""
        shifted = self.leet << 3
        self.assertEqual(shifted, bitmath.Bit(10696))

    def test_right_shift(self):
        """Bits right shifted (>>) are decreased"""
        shifted = self.leet >> 3
        self.assertEqual(shifted, bitmath.Bit(167))

    def test_and(self):
        """Bits and'd (&) are correct"""
        and_fifteen_hundred = self.leet & 1500
        self.assertEqual(and_fifteen_hundred, bitmath.Bit(1304))
        and_orig = self.leet & 1337
        self.assertEqual(and_orig, bitmath.Bit(1337))
        and_thousand = self.leet & 1000
        self.assertEqual(and_thousand, bitmath.Bit(296))
        and_five_hundred = self.leet & 500
        self.assertEqual(and_five_hundred, bitmath.Bit(304))

    def test_or(self):
        """Bits or'd (|) are correct"""
        or_thousand = self.leet | 1000
        self.assertEqual(or_thousand, bitmath.Bit(2041))
        or_five_hundred = self.leet | 500
        self.assertEqual(or_five_hundred, bitmath.Bit(1533))

    def test_xor(self):
        """Bits xor'd (^) are correct"""
        xor_thousand = self.leet ^ 1000
        self.assertEqual(xor_thousand, bitmath.Bit(1745))
        xor_five_hundred = self.leet ^ 500
        self.assertEqual(xor_five_hundred, bitmath.Bit(1229))
