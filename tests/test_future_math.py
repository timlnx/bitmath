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
Test for "future" math operations.

Reference: http://legacy.python.org/dev/peps/pep-0238/
"""

from __future__ import division
from . import TestCase
import bitmath


class TestFutureMath(TestCase):
    def test_bitmath_div_bitmath_is_number(self):
        """truediv: bitmath / bitmath = number"""
        bm1 = bitmath.KiB(1)
        bm2 = bitmath.KiB(2)
        result = bm1 / bm2
        self.assertEqual(result, 0.5)
        self.assertIs(type(result), float)

    def test_bitmath_div_number_is_bitmath(self):
        """truediv: bitmath / number = bitmath"""
        bm1 = bitmath.KiB(1)
        num1 = 2
        result = bm1 / num1
        self.assertEqual(result, bitmath.KiB(0.5))
        self.assertIs(type(result), bitmath.KiB)

    def test_number_div_bitmath_is_number(self):
        """truediv: number / bitmath = number"""
        num1 = 2
        bm1 = bitmath.KiB(1)
        result = num1 / bm1
        self.assertEqual(result, 2.0)
        self.assertIs(type(result), float)

    def test_number_truediv_bitmath_is_number(self):
        """truediv: number // bitmath = number"""
        num1 = 2
        bm1 = bitmath.KiB(1)
        result = bm1.__rdiv__(num1)
        self.assertEqual(result, 2.0)
        self.assertIs(type(result), float)
