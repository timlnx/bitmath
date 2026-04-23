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
        """truediv: number / bitmath = number"""
        num1 = 2
        bm1 = bitmath.KiB(1)
        result = bm1.__rtruediv__(num1)
        self.assertEqual(result, 2.0)
        self.assertIs(type(result), float)

    # -- Floor division ------------------------------------------------

    def test_bitmath_floordiv_bitmath_is_int(self):
        """floordiv: bitmath // bitmath = int (whole divisions)"""
        result = bitmath.GiB(1) // bitmath.MiB(300)
        self.assertEqual(result, 3)
        self.assertIs(type(result), int)

    def test_bitmath_floordiv_bitmath_exact_fit(self):
        """floordiv: exact multiple yields exact int"""
        result = bitmath.GiB(1) // bitmath.MiB(1)
        self.assertEqual(result, 1024)
        self.assertIs(type(result), int)

    def test_bitmath_floordiv_number_preserves_lhs_type(self):
        """floordiv: bitmath // num returns LHS type"""
        result = bitmath.KiB(6) // 4
        self.assertIs(type(result), bitmath.KiB)
        # 6 KiB = 6144 bytes; 6144 // 4 = 1536 bytes = 1.5 KiB
        self.assertEqual(result, bitmath.KiB(1.5))

    # -- Modulo --------------------------------------------------------

    def test_bitmath_mod_bitmath_preserves_lhs_type(self):
        """mod: bitmath % bitmath returns LHS type"""
        result = bitmath.GiB(1) % bitmath.MiB(300)
        self.assertIs(type(result), bitmath.GiB)
        # 1 GiB = 1073741824 bytes; 1073741824 % (300*1048576) = 130023424 bytes
        self.assertEqual(result.bytes, 130023424.0)

    def test_bitmath_mod_bitmath_exact_fit_is_zero(self):
        """mod: exact multiple yields zero in LHS unit"""
        result = bitmath.GiB(1) % bitmath.MiB(1)
        self.assertIs(type(result), bitmath.GiB)
        self.assertEqual(result.bytes, 0)

    def test_bitmath_mod_number_preserves_lhs_type(self):
        """mod: bitmath % num returns LHS type"""
        result = bitmath.KiB(5) % 1024
        self.assertIs(type(result), bitmath.KiB)

    def test_mod_roundtrip_identity(self):
        """(a // b) * b + (a % b) == a"""
        a = bitmath.GiB(1)
        b = bitmath.MiB(300)
        q = a // b
        r = a % b
        self.assertEqual((q * b) + r, a)

    # -- divmod --------------------------------------------------------

    def test_bitmath_divmod_bitmath(self):
        """divmod(bitmath, bitmath) = (int, bitmath of LHS type)"""
        q, r = divmod(bitmath.GiB(1), bitmath.MiB(300))
        self.assertEqual(q, 3)
        self.assertIs(type(q), int)
        self.assertIs(type(r), bitmath.GiB)
        self.assertEqual(r.bytes, 130023424.0)

    def test_bitmath_divmod_exact_fit(self):
        """divmod on exact multiple: remainder is zero"""
        q, r = divmod(bitmath.GiB(10), bitmath.MiB(256))
        self.assertEqual(q, 40)
        self.assertEqual(r.bytes, 0)
