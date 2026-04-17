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
Test the argparse 'BitmathType' integration
"""

from . import TestCase
import bitmath
from bitmath.integrations.bmargparse import BitmathType
import argparse
import shlex


class TestArgparseType(TestCase):
    def setUp(self):
        """Needful for the tests"""
        # A simple one-argument parser that only accept one value.
        self.parser_one_arg = argparse.ArgumentParser()
        self.parser_one_arg.add_argument("--one-arg", type=BitmathType)

        # This parser take one argument, '--two-args'. It requires two values.
        self.parser_two_args = argparse.ArgumentParser()
        self.parser_two_args.add_argument("--two-args", type=BitmathType,
                                          nargs=2)

    def _parse_one_arg(self, arg_str):
        return self.parser_one_arg.parse_args(shlex.split(arg_str))

    def _parse_two_args(self, arg_str):
        return self.parser_two_args.parse_args(shlex.split(arg_str))

    def test_BitmathType_good_one_arg(self):
        """Argparse: BitmathType - Works when given a correct parameter"""
        args = "--one-arg 1000EB"
        result = self._parse_one_arg(args)
        self.assertEqual(bitmath.EB(1000), result.one_arg)

    def test_BitmathType_good_two_args(self):
        """Argparse: BitmathType - Works when given two correct parameters"""
        args = "--two-args 1337B 0.001GiB"
        result = self._parse_two_args(args)
        self.assertEqual(len(result.two_args), 2)
        self.assertIn(bitmath.Byte(1337), result.two_args)
        self.assertIn(bitmath.GiB(0.001), result.two_args)

    def test_BitmathType_bad_wtfareyoudoing(self):
        """Argparse: BitmathType - Notices when horrendously incorrect args are provided"""
        args = "--one-arg 2098329324kdsjflksdjf"
        with self.assertRaises(SystemExit):
            self._parse_one_arg(args)

    def test_BitmathType_good_spaces_in_value(self):
        """Argparse: BitmathType - 'Quoted values' can be separated from the units by whitespace"""
        args = "--two-args '100 MiB' '200 KiB'"
        result = self._parse_two_args(args)
        self.assertEqual(len(result.two_args), 2)
        self.assertIn(bitmath.MiB(100), result.two_args)
        self.assertIn(bitmath.KiB(200), result.two_args)

    def test_BitmathType_bad_spaces_in_value(self):
        """Argparse: BitmathType - Unquoted values separated from their units are detected"""
        args = "--one-arg 1337 B"
        with self.assertRaises(SystemExit):
            self._parse_one_arg(args)
