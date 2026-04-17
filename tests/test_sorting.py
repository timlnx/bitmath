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
Test proper sorting operations
"""

from . import TestCase
import bitmath


class TestSorting(TestCase):
    def test_sort_homogeneous_list(self):
        """Same types in a list can be sorted properly"""
        first = bitmath.kB(0)
        second = bitmath.kB(1337)
        third = bitmath.kB(2048)
        fourth = bitmath.kB(96783)
        # Put the objects into the array in 'random' order
        unsorted_list = [fourth, second, first, third]
        sorted_list = sorted(unsorted_list)
        self.assertIs(sorted_list[0], first)
        self.assertIs(sorted_list[1], second)
        self.assertIs(sorted_list[2], third)
        self.assertIs(sorted_list[3], fourth)

    def test_sort_heterogeneous_list(self):
        """Different types in a list can be sorted properly

Define these with the bytes keyword so we don't lose our minds trying
to figure out if the results are correct."""
        first = bitmath.KiB(bytes=0)
        second = bitmath.GiB(bytes=1337)
        third = bitmath.Eb(bytes=2048)
        fourth = bitmath.Byte(bytes=96783)
        unsorted_list = [fourth, second, first, third]
        sorted_list = sorted(unsorted_list)
        self.assertIs(sorted_list[0], first)
        self.assertIs(sorted_list[1], second)
        self.assertIs(sorted_list[2], third)
        self.assertIs(sorted_list[3], fourth)

    def test_sort_key_bytes(self):
        """Bitmath types can be sorted by 'bytes' attribute"""
        first = bitmath.kB(0)
        second = bitmath.kB(1337)
        third = bitmath.kB(2048)
        fourth = bitmath.kB(96783)
        unsorted_list = [fourth, second, first, third]
        sorted_list = sorted(unsorted_list, key=lambda x: x.bytes)
        self.assertIs(sorted_list[0], first)
        self.assertIs(sorted_list[1], second)
        self.assertIs(sorted_list[2], third)
        self.assertIs(sorted_list[3], fourth)

    def test_sort_key_bits(self):
        """Bitmath types can be sorted by 'bits' attribute"""
        first = bitmath.kB(0)
        second = bitmath.kB(1337)
        third = bitmath.kB(2048)
        fourth = bitmath.kB(96783)
        unsorted_list = [fourth, second, first, third]
        sorted_list = sorted(unsorted_list, key=lambda x: x.bits)
        self.assertIs(sorted_list[0], first)
        self.assertIs(sorted_list[1], second)
        self.assertIs(sorted_list[2], third)
        self.assertIs(sorted_list[3], fourth)

    def test_sort_key_value(self):
        """Same types can be sorted by 'value' attribute

This does not work on heterogeneous collections! The 'value' attribute
varies between different bitmath types even if they are of equivalent
size because it is the shortened representation of that prefix
unit."""
        first = bitmath.kB(0)
        second = bitmath.kB(1337)
        third = bitmath.kB(2048)
        fourth = bitmath.kB(96783)
        unsorted_list = [fourth, second, first, third]
        sorted_list = sorted(unsorted_list, key=lambda x: x.value)
        self.assertIs(sorted_list[0], first)
        self.assertIs(sorted_list[1], second)
        self.assertIs(sorted_list[2], third)
        self.assertIs(sorted_list[3], fourth)
