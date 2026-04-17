# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright © 2015 Tim Case <timbielawa@gmail.com>
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
Test the __init__ method
"""

from . import TestCase
import bitmath


class TestInit(TestCase):
    def test___init__invalid_input_types(self):
        """__init__: can identify (in)valid input parameters, raise ValueError if detected"""
        invalid_inputs = ["one hundred", 100 + 6j, None]
        for invalid_input in invalid_inputs:
            with self.assertRaises(ValueError):
                bitmath.best_prefix(invalid_input)

    def test___init_multiple_kwargs(self):
        """__init__: respects argument mutual exclusivity"""
        # A 100 Byte object can be initialized with any *single* one
        # of these pairs:
        multi_kwargs = {
            "value": 100,  # bitmath.Byte(100)
            "bytes": 100,  # bitmath.Byte(100)
            "bits": 800  # bitmath.Bit(bytes=100)
        }

        with self.assertRaises(ValueError):
            bitmath.Byte(**multi_kwargs)

    def test___init__valid_inputs(self):
        """__init__: accepts valid inputs"""
        inputs = [
            # Comments illustrate what the initialization calls look
            # like after the interpreter expands all the *arg/**kwarg
            # parameters.
            #
            # All pairs are equivalent to Byte(100) (used in the test
            # assertion, below)
            ((100,), dict()),  # Byte(100)
            (tuple(), {"value": 100}),  # Byte(value=100)
            (tuple(), {"bytes": 100}),  # Byte(bytes=100)
            (tuple(), {"bits": 800})  # Byte(bits=800)
        ]

        for args, kwargs in inputs:
            self.assertEqual(bitmath.Byte(*args, **kwargs), bitmath.Byte(100))
