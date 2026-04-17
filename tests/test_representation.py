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
Tests to verify that string representations are accurate
"""

from . import TestCase
import bitmath


class TestRepresentation(TestCase):
    def setUp(self):
        self.kib = bitmath.KiB(1)
        self.kib_repr = 'KiB(1.0)'
        self.kib_str = '1.0 KiB'
        self.kib_unit = 'KiB'
        self.kib_system = 'NIST'
        self.kib_bin = '0b10000000000000'
        self.kib_binary = self.kib_bin
        self.kib_power = 10
        self.kib_base = 2

        self.half_mib = bitmath.MiB(0.5)
        self.half_mib_repr = 'MiB(0.5)'
        self.half_mib_str = '0.5 MiB'

        self.kB = bitmath.kB(1)
        self.kB_unit = 'kB'
        self.kb_system = 'SI'

        self.kib_str_changed = 'KiB 1.000'

    def test_kB_unit(self):
        """kB(1).unit is kB"""
        self.assertEqual(self.kib.unit, self.kib_unit)

    def test_kB_system(self):
        """kB(1).system is SI"""
        self.assertEqual(self.kib.system, self.kib_system)

    def test_kib_unit(self):
        """KiB(1).unit is KiB"""
        self.assertEqual(self.kib.unit, self.kib_unit)

    def test_kib_system(self):
        """KiB(1).system is NIST"""
        self.assertEqual(self.kib.system, self.kib_system)

    def test_kib_binary(self):
        """KiB(1).binary is binary"""
        self.assertEqual(self.kib.binary, self.kib_binary)

    def test_kib_bin(self):
        """KiB(1).bin (binary alias) is binary"""
        self.assertEqual(self.kib.bin, self.kib_bin)

    def test_kib_base(self):
        """KiB(1).base is 2"""
        self.assertEqual(self.kib.base, self.kib_base)

    def test_kib_power(self):
        """KiB(1).power (binary alias) is 10"""
        self.assertEqual(self.kib.power, self.kib_power)

    def test_whole_kib_repr(self):
        """KiB(1) looks correct in a terminal"""
        self.assertEqual(repr(self.kib), self.kib_repr)

    def test_whole_kib_str(self):
        """KiB(1) looks correct as a string"""
        self.assertEqual(str(self.kib), self.kib_str)

    def test_half_mib_repr(self):
        """MiB(0.5) looks correct in a terminal"""
        self.assertEqual(repr(self.half_mib), self.half_mib_repr)

    def test_half_mib_str(self):
        """MiB(0.5) looks correct as a string"""
        self.assertEqual(str(self.half_mib), self.half_mib_str)

    ##################################################################
    # Test custom formatting
    def test_print_two_digits_precision(self):
        """MiB(1/3.0) prints out with two digits of precision"""
        expected_result = "0.33MiB"
        fmt_str = "{value:.2f}{unit}"
        third_MiB = bitmath.MiB(1 / 3.0)
        actual_result = third_MiB.format(fmt_str)
        self.assertEqual(expected_result, actual_result)

    def test_print_scientific_four_digits_precision(self):
        """MiB(102.4754) prints out with four digits of precision"""
        expected_result = "102.5MiB"
        fmt_str = "{value:.4g}{unit}"
        third_MiB = bitmath.MiB(102.4754)
        actual_result = third_MiB.format(fmt_str)
        self.assertEqual(expected_result, actual_result)

    def test_longer_formatting_string(self):
        """KiB(12345) as a MiB (12.0556640625) truncates to 5 digits"""
        expected_result = "12.05566 MiB"
        fmt_str = "{value:.5f} {unit}"
        instance = bitmath.KiB(12345).to_MiB()
        actual_result = instance.format(fmt_str)
        self.assertEqual(expected_result, actual_result)

    def test_change_format_string(self):
        """KiB(1.0) looks right if changing fmt str in bitmath.KiB

NOTE: This does NOT make use of the bitmath.format context
manager. There is a separate test suite for that: test_context_manager"""
        orig_fmt_str = bitmath.format_string
        bitmath.format_string = "{unit} {value:.3f}"
        kib = bitmath.KiB(1)
        self.assertEqual(self.kib_str_changed, str(kib))
        bitmath.format_string = orig_fmt_str

    def test_print_byte_singular(self):
        """Byte(1.0) prints out units in singular form"""
        expected_result = "1Byte"
        fmt_str = "{value:.2g}{unit}"
        one_Byte = bitmath.Byte(1.0)
        actual_result = one_Byte.format(fmt_str)
        self.assertEqual(expected_result, actual_result)
