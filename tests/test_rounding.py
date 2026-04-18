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
Tests for math.floor(), math.ceil(), and round() on bitmath instances
"""

import math
from . import TestCase
import bitmath


class TestFloor(TestCase):
    def test_floor_fractional_returns_same_type(self):
        """math.floor() returns the same unit type"""
        result = math.floor(bitmath.MiB(1.9))
        self.assertIsInstance(result, bitmath.MiB)

    def test_floor_rounds_down(self):
        """math.floor() rounds the prefix value down"""
        self.assertEqual(math.floor(bitmath.MiB(1.9)), bitmath.MiB(1))

    def test_floor_whole_number_unchanged(self):
        """math.floor() on a whole prefix value returns that value"""
        self.assertEqual(math.floor(bitmath.KiB(3)), bitmath.KiB(3))

    def test_floor_negative_rounds_toward_negative_infinity(self):
        """math.floor() on a negative value rounds toward negative infinity"""
        self.assertEqual(math.floor(bitmath.GiB(-1.1)), bitmath.GiB(-2))

    def test_floor_division_result(self):
        """math.floor() on a division result produces integer prefix value"""
        self.assertEqual(math.floor(bitmath.KiB(1) / 3), bitmath.KiB(0))

    def test_floor_preserves_unit_across_types(self):
        """math.floor() works across all unit types"""
        for unit in [bitmath.Byte, bitmath.KiB, bitmath.MiB, bitmath.GiB,
                     bitmath.kB, bitmath.MB]:
            result = math.floor(unit(1.7))
            self.assertIsInstance(result, unit)
            self.assertEqual(result, unit(1))


class TestCeil(TestCase):
    def test_ceil_fractional_returns_same_type(self):
        """math.ceil() returns the same unit type"""
        result = math.ceil(bitmath.MiB(1.1))
        self.assertIsInstance(result, bitmath.MiB)

    def test_ceil_rounds_up(self):
        """math.ceil() rounds the prefix value up"""
        self.assertEqual(math.ceil(bitmath.MiB(1.1)), bitmath.MiB(2))

    def test_ceil_whole_number_unchanged(self):
        """math.ceil() on a whole prefix value returns that value"""
        self.assertEqual(math.ceil(bitmath.KiB(3)), bitmath.KiB(3))

    def test_ceil_negative_rounds_toward_zero(self):
        """math.ceil() on a negative value rounds toward zero"""
        self.assertEqual(math.ceil(bitmath.GiB(-1.9)), bitmath.GiB(-1))

    def test_ceil_division_result(self):
        """math.ceil() on a division result rounds up to next prefix unit"""
        self.assertEqual(math.ceil(bitmath.KiB(1) / 3), bitmath.KiB(1))

    def test_ceil_preserves_unit_across_types(self):
        """math.ceil() works across all unit types"""
        for unit in [bitmath.Byte, bitmath.KiB, bitmath.MiB, bitmath.GiB,
                     bitmath.kB, bitmath.MB]:
            result = math.ceil(unit(1.2))
            self.assertIsInstance(result, unit)
            self.assertEqual(result, unit(2))


class TestRound(TestCase):
    def test_round_no_ndigits_returns_same_type(self):
        """round() with no ndigits returns the same unit type"""
        result = round(bitmath.GiB(3.7))
        self.assertIsInstance(result, bitmath.GiB)

    def test_round_no_ndigits_rounds_to_nearest(self):
        """round() with no ndigits rounds to the nearest integer prefix value"""
        self.assertEqual(round(bitmath.GiB(3.7)), bitmath.GiB(4))
        self.assertEqual(round(bitmath.GiB(3.2)), bitmath.GiB(3))

    def test_round_with_ndigits_returns_same_type(self):
        """round(x, ndigits) returns the same unit type"""
        result = round(bitmath.KiB(1.555), 2)
        self.assertIsInstance(result, bitmath.KiB)

    def test_round_with_ndigits(self):
        """round(x, ndigits) rounds to the specified decimal precision"""
        self.assertEqual(round(bitmath.KiB(1.5), 0), bitmath.KiB(2))
        self.assertEqual(round(bitmath.MiB(2.567), 1), bitmath.MiB(2.6))

    def test_round_whole_number_unchanged(self):
        """round() on a whole prefix value returns that value"""
        self.assertEqual(round(bitmath.MiB(5)), bitmath.MiB(5))

    def test_round_negative_value(self):
        """round() on a negative value rounds to nearest"""
        self.assertEqual(round(bitmath.GiB(-3.7)), bitmath.GiB(-4))
        self.assertEqual(round(bitmath.GiB(-3.2)), bitmath.GiB(-3))

    def test_floor_ceil_round_not_equal_for_fractional(self):
        """floor, ceil, and round give distinct results for fractional values"""
        val = bitmath.MiB(1.6)
        self.assertEqual(math.floor(val), bitmath.MiB(1))
        self.assertEqual(math.ceil(val), bitmath.MiB(2))
        self.assertEqual(round(val), bitmath.MiB(2))
