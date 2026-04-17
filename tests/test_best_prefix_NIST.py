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
Test for NIST prefix guessing
"""

from . import TestCase
import bitmath


class TestBestPrefixNIST(TestCase):
    ##################################################################
    # These tests verify guessing for cases where the best
    # representation is only one order of magnitude different.

    def test_simple_round_up(self):
        """NIST: 1 GiB (as a MiB()) rounds up into a GiB()"""
        # Represent a Gibibyte as a large MiB
        GiB_in_MiB = bitmath.MiB(1024)
        # This should turn into a GiB
        self.assertIs(type(GiB_in_MiB.best_prefix()), bitmath.GiB)

    def test_simple_round_down(self):
        """NIST: 1 MiB (as a GiB()) rounds down into a MiB()"""
        # Represent one MiB as a small GiB
        MiB_in_GiB = bitmath.GiB(bytes=1048576)
        # This should turn into a MiB
        self.assertIs(type(MiB_in_GiB.best_prefix()), bitmath.MiB)

    ##################################################################
    # These tests verify guessing for cases where the best
    # representation is more than one order of magnitude different.

    def test_multi_oom_round_up(self):
        """NIST: A very large Kibibyte rounds up into a Pibibyte"""
        large_KiB = bitmath.KiB.from_other(bitmath.PiB(1))
        self.assertIs(type(large_KiB.best_prefix()), bitmath.PiB)

    def test_multi_oom_round_down(self):
        """NIST: A very small Pibibyte rounds down into a KibiByte"""
        small_PiB = bitmath.PiB.from_other(bitmath.KiB(1))
        self.assertIs(type(small_PiB.best_prefix()), bitmath.KiB)

    ##################################################################
    # These tests mirror the multi_oom ones, except for extreme cases
    # where even the largest unit available results in values with
    # more than 4 digits left of the radix point.

    def test_extreme_oom_round_up(self):
        """NIST: 2048 EiB (as a KiB()) rounds up into an EiB()"""
        huge_KiB = bitmath.KiB.from_other(bitmath.EiB(1))
        self.assertIs(type(huge_KiB.best_prefix()), bitmath.EiB)

    def test_extreme_oom_round_down(self):
        """NIST: 1 Bit (as a EiB()) rounds down into a Bit()"""
        tiny_EiB = bitmath.EiB.from_other(bitmath.Bit(1))
        self.assertIs(type(tiny_EiB.best_prefix()), bitmath.Bit)

    ##################################################################
    # These tests verify that when we use the preferred prefix 'NIST'
    # we get a NIST type unit back.
    #
    # One test for each case. First, start with an SI unit, second,
    # start with a NIST unit

    def test_best_prefix_prefer_NIST_from_SI(self):
        """NIST: Best prefix honors a NIST preference when starting with an SI unit

Start with an SI (kb) unit and prefer a NIST unit as the result (MiB)
"""
        # Start with kB, an SI unit
        should_be_MiB = bitmath.kB(1600).best_prefix(system=bitmath.NIST)
        self.assertIs(type(should_be_MiB), bitmath.MiB)

    def test_best_prefix_prefer_NIST_from_NIST(self):
        """NIST: Best prefix honors a NIST preference when starting with an NIST unit

Start with a NIST (GiB) unit and prefer a NIST unit as the result (MiB)"""
        # This should be MiB(512.0)
        should_be_MiB = bitmath.GiB(0.5).best_prefix(system=bitmath.NIST)
        self.assertIs(type(should_be_MiB), bitmath.MiB)

    ##################################################################

    def test_best_prefix_NIST_default(self):
        """NIST: Best prefix uses the current system if no preference set

Start with a NIST unit and assert no preference. The default behavior
returns a prefix from the current system family (GiB)"""
        # The MiB is == 1 GiB, conversion happens, and the result is a
        # unit from the same family (GiB)
        should_be_GiB = bitmath.MiB(1024).best_prefix()
        self.assertIs(type(should_be_GiB), bitmath.GiB)

    def test_best_prefix_identical_result(self):
        """NIST: instance.best_prefix returns the same type if nothing changes

Start with a NIST unit that is already prefectly sized, and apply
best_prefix() to it."""
        # This is our perfectly sized unit. No change was required
        should_be_EiB = bitmath.EiB(1).best_prefix()
        self.assertIs(type(should_be_EiB), bitmath.EiB)

        # Let's be thorough and do that one more time
        self.assertIs(type(should_be_EiB.best_prefix()), bitmath.EiB)

    ##################################################################
    # Tests for the utility function bitmath.best_prefix() where
    # SYSTEM=NIST

    def test_bitmath_best_prefix_NIST(self):
        """bitmath.best_prefix return a Kibibyte for 1024"""
        result = bitmath.best_prefix(1024)
        self.assertIs(type(result), bitmath.KiB)

    def test_bitmath_best_prefix_NIST_exbi(self):
        """bitmath.best_prefix return an exbibyte for a huge number of bytes"""
        result = bitmath.best_prefix(1152921504606846977)
        self.assertIs(type(result), bitmath.EiB)
