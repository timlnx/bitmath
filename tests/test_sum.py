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
Tests for bitmath.sum() - issue #103
"""

from . import TestCase
import builtins
import bitmath


class TestSum(TestCase):
    def test_sum_mixed_units_equals_manual_addition(self):
        """bitmath.sum() matches manual chained addition for mixed units"""
        items = [bitmath.Byte(1), bitmath.MiB(1), bitmath.GiB(1)]
        expected = bitmath.Byte(1) + bitmath.MiB(1) + bitmath.GiB(1)
        self.assertEqual(bitmath.sum(items), expected)

    def test_sum_returns_bitmath_instance(self):
        """bitmath.sum() returns a bitmath instance, not a float"""
        result = bitmath.sum([bitmath.Byte(1), bitmath.MiB(1), bitmath.GiB(1)])
        self.assertIsInstance(result, bitmath.Bitmath)

    def test_sum_builtin_now_works(self):
        """built-in sum() now gives correct result via __radd__ identity fix"""
        items = [bitmath.Byte(1), bitmath.MiB(1), bitmath.GiB(1)]
        self.assertEqual(builtins.sum(items), bitmath.sum(items))

    def test_sum_empty_iterable_returns_byte_zero(self):
        """bitmath.sum([]) returns Byte(0) by default"""
        result = bitmath.sum([])
        self.assertEqual(result, bitmath.Byte(0))

    def test_sum_empty_iterable_with_custom_start(self):
        """bitmath.sum([], start=MiB(0)) returns the start value"""
        result = bitmath.sum([], start=bitmath.MiB(0))
        self.assertEqual(result, bitmath.MiB(0))

    def test_sum_custom_start_unit(self):
        """bitmath.sum() with a custom start unit returns that unit type"""
        result = bitmath.sum([bitmath.KiB(1), bitmath.KiB(1)], start=bitmath.MiB(0))
        self.assertIsInstance(result, bitmath.MiB)

    def test_sum_same_units(self):
        """bitmath.sum() works correctly for a list of same-unit instances"""
        result = bitmath.sum([bitmath.KiB(1), bitmath.KiB(2), bitmath.KiB(3)])
        self.assertEqual(result, bitmath.KiB(6))
