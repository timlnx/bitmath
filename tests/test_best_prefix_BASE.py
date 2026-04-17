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
Test for base (Bit/Byte) prefix guessing
"""

from . import TestCase
import bitmath


class TestBestPrefixBASE(TestCase):
    def test_byte_round_down(self):
        """best_prefix_base: 4 Bits (as a Byte()) round down into a Bit()"""
        # Half a byte is 4 bits
        half_byte = bitmath.Byte(bits=4)
        # Byte(0.5) should round down into Bit(4)
        self.assertIs(type(half_byte.best_prefix()), bitmath.Bit)

    def test_bit_round_up(self):
        """best_prefix_base: 2 Bytes (as a Bit()) round up into a Byte()"""
        # Two bytes is 16 bits
        two_bytes = bitmath.Bit(bytes=2)
        # Bit(16) should round up into Byte(2)
        self.assertIs(type(two_bytes.best_prefix()), bitmath.Byte)

    def test_byte_no_rounding(self):
        """best_prefix_base: 1 Byte (as a Byte()) best prefix is still a Byte()"""
        # One whole byte
        one_byte = bitmath.Byte(1)
        # Byte(1.0) should stay the same, Byte(1.0)
        self.assertIs(type(one_byte.best_prefix()), bitmath.Byte)

    def test_best_prefix_with_bitmath_input(self):
        """best_prefix_base: can handle bitmath type inputs"""
        bm1 = bitmath.Byte(1024)
        expected = bitmath.KiB(1)
        self.assertEqual(bitmath.best_prefix(bm1), expected)

    # Negative Tests - reference: github issue #55
    #
    # For instances where x in set { b | 0 <= abs(b) < 8 } where b is
    # number of bits in an instance:
    #
    # * bitmath.best_prefix(Byte(bits=-4)) -> Bit(-4)
    # * bitmath.best_prefix(Byte(bits=4)) -> Bit(4)
    def test_best_prefix_negative_less_than_a_byte(self):
        """best_prefix_base: negative values less than a byte stay as bits"""
        # assert that a Byte of -4 bits yields Bit(-4)
        bm1 = bitmath.Byte(bits=-4)
        expected = bitmath.Bit(-4)
        res = bitmath.best_prefix(bm1)
        # Verify that best prefix math works for negative numbers
        self.assertEqual(res, expected)
        # Verify that best prefix guessed the correct type
        self.assertIs(type(res), bitmath.Bit)

    # For instances where x in set { b | b >= 8 } where b is number of
    # bits in an instance:
    #
    # * bitmath.best_prefix(-10**8) -> MiB(-95.367...)
    # * bitmath.best_prefix(10**8) -> MiB(95.367...)
    def test_best_prefix_negative_huge_numbers(self):
        """best_prefix_base: large negative values retain their prefix unit"""
        positive_result = bitmath.best_prefix(10**8)
        negative_result = bitmath.best_prefix(-10**8)
        # Verify that the best prefix math works for negative and
        # positive numbers
        self.assertEqual(negative_result, -1 * positive_result)
        # Verify that they produce the same type
        self.assertIs(type(negative_result), type(positive_result))
        # Verify that type is what we expect it to be
        self.assertIs(type(negative_result), bitmath.MiB)
