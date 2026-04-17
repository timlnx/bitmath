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
Tests to verify that the formatting context manager works
"""

from . import TestCase
import bitmath


class TestContextManager(TestCase):
    def test_with_format(self):
        """bitmath.format context mgr sets and restores formatting"""
        to_print = [
            bitmath.Byte(101),
            bitmath.KiB(202),
            bitmath.MB(303),
            bitmath.GiB(404),
            bitmath.TB(505),
            bitmath.PiB(606),
            bitmath.EB(707)
        ]

        str_reps = [
            "101.00-Byte",
            "202.00-KiB",
            "303.00-MB",
            "404.00-GiB",
            "505.00-TB",
            "606.00-PiB",
            "707.00-EB"
        ]

        # Make sure formatting looks right BEFORE the context manager
        self.assertEqual(str(bitmath.KiB(1.337)), "1.337 KiB")

        with bitmath.format("{value:.2f}-{unit}"):
            for (inst, inst_str) in zip(to_print, str_reps):
                self.assertEqual(str(inst), inst_str)

        # Make sure formatting looks right AFTER the context manager
        self.assertEqual(str(bitmath.KiB(1.337)), "1.337 KiB")

    def test_print_byte_plural(self):
        """Byte(3.0) prints out units in plural form"""
        expected_result = "3Bytes"
        fmt_str = "{value:.1g}{unit}"
        three_Bytes = bitmath.Byte(3.0)

        with bitmath.format(plural=True):
            actual_result = three_Bytes.format(fmt_str)
            self.assertEqual(expected_result, actual_result)

    def test_print_byte_plural_fmt_in_mgr(self):
        """Byte(3.0) prints out units in plural form, setting the fmt str in the mgr"""
        expected_result = "3Bytes"

        with bitmath.format(fmt_str="{value:.1g}{unit}", plural=True):
            three_Bytes = bitmath.Byte(3.0)
            actual_result = str(three_Bytes)
            self.assertEqual(expected_result, actual_result)

    def test_print_GiB_plural_fmt_in_mgr(self):
        """TiB(1/3.0) prints out units in plural form, setting the fmt str in the mgr"""
        expected_result = "3Bytes"

        with bitmath.format(fmt_str="{value:.1g}{unit}", plural=True):
            three_Bytes = bitmath.Byte(3.0)
            actual_result = str(three_Bytes)
            self.assertEqual(expected_result, actual_result)

    def test_print_GiB_singular_fmt_in_mgr(self):
        """TiB(1/3.0) prints out units in singular form, setting the fmt str in the mgr"""
        expected_result = "341.3GiB"

        with bitmath.format(fmt_str="{value:.1f}{unit}"):
            third_tibibyte = bitmath.TiB(1 / 3.0).best_prefix()
            actual_result = str(third_tibibyte)
            self.assertEqual(expected_result, actual_result)
