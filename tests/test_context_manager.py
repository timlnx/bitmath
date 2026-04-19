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
            "101.00-B",
            "202.00-KiB",
            "303.00-MB",
            "404.00-GiB",
            "505.00-TB",
            "606.00-PiB",
            "707.00-EB"
        ]

        # Make sure formatting looks right BEFORE the context manager
        self.assertEqual(str(bitmath.KiB(1.337)), "1.34 KiB")

        with bitmath.format("{value:.2f}-{unit}"):
            for (inst, inst_str) in zip(to_print, str_reps):
                self.assertEqual(str(inst), inst_str)

        # Make sure formatting looks right AFTER the context manager
        self.assertEqual(str(bitmath.KiB(1.337)), "1.34 KiB")

    def test_print_byte_plural(self):
        """Byte(3.0) prints out units in plural form"""
        expected_result = "3B"
        fmt_str = "{value:.1g}{unit}"
        three_Bytes = bitmath.Byte(3.0)

        with bitmath.format(plural=True):
            actual_result = three_Bytes.format(fmt_str)
            self.assertEqual(expected_result, actual_result)

    def test_print_byte_plural_fmt_in_mgr(self):
        """Byte(3.0) prints out units in plural form, setting the fmt str in the mgr"""
        expected_result = "3B"

        with bitmath.format(fmt_str="{value:.1g}{unit}", plural=True):
            three_Bytes = bitmath.Byte(3.0)
            actual_result = str(three_Bytes)
            self.assertEqual(expected_result, actual_result)

    def test_print_GiB_plural_fmt_in_mgr(self):
        """GiB(3.0) prints out units in plural form, setting the fmt str in the mgr"""
        expected_result = "3GiBs"

        with bitmath.format(fmt_str="{value:.1g}{unit}", plural=True):
            three_GiB = bitmath.GiB(3.0)
            actual_result = str(three_GiB)
            self.assertEqual(expected_result, actual_result)

    def test_print_GiB_singular_fmt_in_mgr(self):
        """TiB(1/3.0) prints out units in singular form, setting the fmt str in the mgr"""
        expected_result = "341.3GiB"

        with bitmath.format(fmt_str="{value:.1f}{unit}"):
            third_tibibyte = bitmath.TiB(1 / 3.0).best_prefix()
            actual_result = str(third_tibibyte)
            self.assertEqual(expected_result, actual_result)

    def test_bestprefix_in_context_manager(self):
        """bestprefix=True causes str() to render the best human-readable prefix"""
        with bitmath.format(bestprefix=True):
            result = str(bitmath.MiB(1024))
        self.assertEqual(result, "1.00 GiB")

    def test_bestprefix_restores_after_context(self):
        """bestprefix is not active outside the context manager"""
        with bitmath.format(bestprefix=True):
            pass
        self.assertEqual(str(bitmath.MiB(1024)), "1024.00 MiB")

    def test_bestprefix_with_fmt_str(self):
        """bestprefix=True combined with fmt_str applies the format to the converted unit"""
        with bitmath.format(fmt_str="{value:.2f} {unit}", bestprefix=True):
            result = str(bitmath.KiB(2048))
        self.assertEqual(result, "2.00 MiB")

    def test_format_restored_after_exception(self):
        """format_string is restored to default even when an exception is raised"""
        original = bitmath.format_string
        try:
            with bitmath.format(fmt_str="{value:.2f} {unit}"):
                raise ValueError("boom")
        except ValueError:
            pass
        self.assertEqual(bitmath.format_string, original)
        self.assertEqual(str(bitmath.KiB(1)), "1.00 KiB")

    def test_nested_context_managers(self):
        """Nested format contexts correctly save and restore enclosing context state"""
        with bitmath.format(fmt_str="{value:.1f} {unit}"):
            self.assertEqual(str(bitmath.KiB(1)), "1.0 KiB")
            with bitmath.format(fmt_str="{value:.3f} {unit}"):
                self.assertEqual(str(bitmath.KiB(1)), "1.000 KiB")
            self.assertEqual(str(bitmath.KiB(1)), "1.0 KiB")
        self.assertEqual(str(bitmath.KiB(1)), "1.00 KiB")
