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
Tests to verify that type properties are accessable and immutable
"""

from . import TestCase
import bitmath


class TestAttributeProperties(TestCase):

    def setUp(self):
        self.kib = bitmath.KiB(1)
        self.kib_bits = 8192
        self.kib_bytes = 1024
        self.kib_value = 1

    def test_read_bits(self):
        """Read the 'bits' property of a bitmath type"""
        self.assertEqual(self.kib.bits, self.kib_bits)

    def test_read_bytes(self):
        """Read the 'bytes' property of a bitmath type"""
        self.assertEqual(self.kib.bytes, self.kib_bytes)

    def test_read_value(self):
        """Read the 'value' property of a bitmath type"""
        self.assertEqual(self.kib.value, self.kib_value)

    def test_write_property_fails(self):
        """bitmath type's properties are read-only"""
        with self.assertRaises(AttributeError):
            self.kib.value += 42

    def test_ZiB_property(self):
        """ZiB property returns a ZiB instance"""
        self.assertIsInstance(self.kib.ZiB, bitmath.ZiB)

    def test_YiB_property(self):
        """YiB property returns a YiB instance"""
        self.assertIsInstance(self.kib.YiB, bitmath.YiB)

    def test_Zib_property(self):
        """Zib property returns a Zib instance"""
        self.assertIsInstance(self.kib.Zib, bitmath.Zib)

    def test_Yib_property(self):
        """Yib property returns a Yib instance"""
        self.assertIsInstance(self.kib.Yib, bitmath.Yib)
