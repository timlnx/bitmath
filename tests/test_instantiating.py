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


"""Test that bitmath instances can only be instantiated with 0 or 1
arguments. Make sure the base 'bitmath.Bitmath' class can not be
instantiated either.
"""

from . import TestCase
import bitmath


class TestInstantiating(TestCase):
    ##################################################################
    # First, the simple passing tests

    def test_init_no_arguments(self):
        """Instantiation works with no arguments"""
        bm = bitmath.Byte()
        # An instance with 0 arguments will have a value of 0
        self.assertEqual(bm, bitmath.Byte(0))

    def test_init_value(self):
        """Instantiation works with only 'value' provided"""
        bm1 = bitmath.Byte(1)
        bm2 = bitmath.Byte(value=1)

        # These instances will be equivalent to each other and
        # congruent to int(1)
        self.assertEqual(bm1, bm2)
        self.assertEqual(bm1, int(1))
        self.assertEqual(bm2, int(1))

    def test_init_bytes(self):
        """Instantiation works with the 'bytes' kw arg"""
        bm = bitmath.Byte(bytes=1024)

        # 1024 bytes is 1 KiB, these should be equal
        self.assertEqual(bm, bitmath.KiB(1))
        self.assertEqual(bm.bytes, 1024)

    def test_init_bits(self):
        """Instantiation works with the 'bits' kw arg"""
        bm = bitmath.Byte(bits=8)

        # 8 bits is 1 byte, these should be equal
        self.assertEqual(bm, bitmath.Byte(1))

    ##################################################################
    # Now, the invalid uses

    # value and bytes
    def test_bad_init_value_bytes(self):
        """Instantiation fails if value and bytes are both provided"""
        with self.assertRaises(ValueError):
            bitmath.Byte(value=1, bytes=1)

    # value and bits
    def test_bad_init_value_bits(self):
        """Instantiation fails if value and bits are both provided"""
        with self.assertRaises(ValueError):
            bitmath.Byte(value=1, bits=1)

    # bytes and bits
    def test_bad_init_bytes_bits(self):
        """Instantiation fails if bytes and bits are both provided"""
        with self.assertRaises(ValueError):
            bitmath.Byte(bytes=1, bits=1)

    # value and bytes and bits
    def test_bad_init_value_bytes_bits(self):
        """Instantiation fails if value and bytes and bits are all provided"""
        with self.assertRaises(ValueError):
            bitmath.Byte(value=1, bytes=1, bits=1)

    ##################################################################
    # Double check we can't create rogue instances of bitmath.Bitmath
    def test_bitmath_Bitmath_cannot_be_instantiated(self):
        """Instantiation fails if we try to instantiate bitmath.Bitmath"""
        with self.assertRaises(NotImplementedError):
            bitmath.Bitmath(1337)

    ##################################################################
    # ZiB, YiB, Zib, Yib — NIST large units added in 2.0.0

    def test_ZiB_instantiation(self):
        """ZiB can be instantiated"""
        self.assertIsInstance(bitmath.ZiB(1), bitmath.ZiB)

    def test_YiB_instantiation(self):
        """YiB can be instantiated"""
        self.assertIsInstance(bitmath.YiB(1), bitmath.YiB)

    def test_Zib_instantiation(self):
        """Zib can be instantiated"""
        self.assertIsInstance(bitmath.Zib(1), bitmath.Zib)

    def test_Yib_instantiation(self):
        """Yib can be instantiated"""
        self.assertIsInstance(bitmath.Yib(1), bitmath.Yib)

    def test_ZiB_in_all_unit_types(self):
        """ZiB is listed in ALL_UNIT_TYPES"""
        self.assertIn('ZiB', bitmath.ALL_UNIT_TYPES)

    def test_YiB_in_all_unit_types(self):
        """YiB is listed in ALL_UNIT_TYPES"""
        self.assertIn('YiB', bitmath.ALL_UNIT_TYPES)

    def test_Zib_in_all_unit_types(self):
        """Zib is listed in ALL_UNIT_TYPES"""
        self.assertIn('Zib', bitmath.ALL_UNIT_TYPES)

    def test_Yib_in_all_unit_types(self):
        """Yib is listed in ALL_UNIT_TYPES"""
        self.assertIn('Yib', bitmath.ALL_UNIT_TYPES)
