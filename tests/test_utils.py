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
Test utility functions
"""

from . import TestCase
import bitmath


class TestUtils(TestCase):
    def test_capitalize_first_normal_word(self):
        """capitalize_first upcases just the first letter in a word"""
        word1 = "foo"
        expected1 = "Foo"
        self.assertEqual(
            bitmath.capitalize_first(word1),
            expected1)

        word2 = "foO"
        expected2 = "FoO"
        self.assertEqual(
            bitmath.capitalize_first(word2),
            expected2)

    def test_capitalize_first_starts_with_number(self):
        """capitalize_first doesn't change anything if the input begins with a number"""
        word = "1foo"
        expected = "1foo"
        self.assertEqual(
            bitmath.capitalize_first(word),
            expected)

    def test_capitalize_first_already_capped(self):
        """capitalize_first doesn't change anything if the input is already correct"""
        word = "Foo"
        expected = "Foo"
        self.assertEqual(
            bitmath.capitalize_first(word),
            expected)
