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
Test the command line tool
"""

from . import TestCase
import bitmath


class TestCli(TestCase):
    def test_cli_script_main_no_options(self):
        """CLI script returns nothing if no input is given"""
        results = bitmath.cli_script_main([])
        self.assertEqual(results, [])

    def test_cli_script_main_no_units(self):
        """CLI script works if no to/from units are provided"""
        args = ['100', '1024']
        results = bitmath.cli_script_main(args)
        self.assertEqual(results[0], bitmath.Byte(100))
        self.assertEqual(results[1], bitmath.KiB(1))

    def test_cli_script_main_to_unit(self):
        """CLI script returns correct TO units"""
        args = ['-t', 'MiB', '1048576']
        results = bitmath.cli_script_main(args)
        self.assertEqual(results[0], bitmath.MiB(1))
        self.assertIs(type(results[0]), bitmath.MiB)

    def test_cli_script_main_from_unit(self):
        """CLI script returns correct if given FROM units"""
        args = ['-f', 'MiB', '0.5']
        # Testing FROM 0.5 MiB TO best human readable unit (512 KiB)
        results = bitmath.cli_script_main(args)
        self.assertEqual(results[0], bitmath.KiB(512))
        self.assertIs(type(results[0]), bitmath.KiB)

    def test_cli_script_main_from_and_to_unit(self):
        """CLI script returns correct if given FROM and TO units"""
        args = ['-f', 'MiB', '-t', 'Byte', '1']
        # Testing FROM 1 MiB TO equivalent Bytes
        results = bitmath.cli_script_main(args)
        self.assertEqual(results[0], bitmath.Byte(1048576))
        self.assertIs(type(results[0]), bitmath.Byte)
