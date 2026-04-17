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
Test for SI prefix guessing
"""

from . import TestCase
import bitmath


class TestBestPrefixSI(TestCase):
    ##################################################################
    # These tests verify guessing for cases where the best
    # representation is only one order of magnitude different.

    def test_simple_round_up(self):
        """SI: 1 GB (as a MB()) rounds up into a GB()"""
        # Represent a Gigabyte as a large MB
        GB_in_MB = bitmath.MB(1024)
        # This should turn into a GB
        self.assertIs(type(GB_in_MB.best_prefix()), bitmath.GB)

    def test_simple_round_down(self):
        """SI: 1 MB (as a GB()) rounds down into a MB()"""
        # Represent one MB as a small GB
        MB_in_GB = bitmath.GB(bytes=1048576)
        # This should turn into a MB
        self.assertIs(type(MB_in_GB.best_prefix()), bitmath.MB)

    ##################################################################
    # These tests verify guessing for cases where the best
    # representation is more than one order of magnitude different.

    def test_multi_oom_round_up(self):
        """SI: A very large Kilobyte rounds up into a Petabyte"""
        large_kB = bitmath.kB.from_other(bitmath.PB(1))
        self.assertIs(type(large_kB.best_prefix()), bitmath.PB)

    def test_multi_oom_round_down(self):
        """SI: A very small Petabyte rounds down into a Kilobyte"""
        small_PB = bitmath.PB.from_other(bitmath.kB(1))
        self.assertIs(type(small_PB.best_prefix()), bitmath.kB)

    ##################################################################
    # These tests mirror the multi_oom ones, except for extreme cases
    # where even the largest unit available results in values with
    # more than 4 digits left of the radix point.

    def test_extreme_oom_round_up(self):
        """SI: 2048 EB (as a kB()) rounds up into an EB()"""
        huge_kB = bitmath.kB.from_other(bitmath.EB(1))
        self.assertIs(type(huge_kB.best_prefix()), bitmath.EB)

    def test_extreme_oom_round_down(self):
        """SI: 1 Bit (as a EB()) rounds down into a Bit()"""
        tiny_EB = bitmath.EB.from_other(bitmath.Bit(1))
        self.assertIs(type(tiny_EB.best_prefix()), bitmath.Bit)

    ##################################################################
    # These tests verify that when we use the preferred prefix 'SI'
    # we get a SI type unit back which required a new prefix
    #
    # One test for each case. First, start with an SI unit, second,
    # start with a NIST unit

    def test_best_prefix_prefer_SI_from_SI(self):
        """SI: Best prefix honors a SI preference when starting with an SI unit

Start with an SI (kb) unit and prefer a SI unit as the result (MB)
"""
        # Start with kB, a SI unit
        should_be_MB = bitmath.kB(1600).best_prefix(system=bitmath.SI)
        self.assertIs(type(should_be_MB), bitmath.MB)

    def test_best_prefix_prefer_SI_from_NIST(self):
        """SI: Best prefix honors a SI preference when starting with a NIST unit

Start with a NIST (GiB) unit and prefer a SI unit as the result (MB)"""
        # Start with GiB, an NIST unit
        should_be_MB = bitmath.GiB(0.5).best_prefix(system=bitmath.SI)
        self.assertIs(type(should_be_MB), bitmath.MB)

    ##################################################################

    def test_best_prefix_SI_default(self):
        """SI: Best prefix uses the current system if no preference set

Start with a SI unit and assert no preference. The default behavior
returns a prefix from the current system family (GB)"""
        # The MB is == 1 GB, conversion happens, and the result is a
        # unit from the same family (GB)
        should_be_GB = bitmath.MB(1000).best_prefix()
        self.assertIs(type(should_be_GB), bitmath.GB)

    def test_best_prefix_identical_result(self):
        """SI: best_prefix returns the same type when nothing changes

Start with a SI unit that is already prefectly sized, and apply
best_prefix() to it. again"""
        # This is our perfectly sized unit. No change was required
        should_be_EB = bitmath.EB(1).best_prefix()
        self.assertIs(type(should_be_EB), bitmath.EB)

        # Let's be thorough and do that one more time
        self.assertIs(type(should_be_EB.best_prefix()), bitmath.EB)

    ##################################################################
    # Tests for the utility function bitmath.best_prefix() where
    # SYSTEM=SI

    def test_bitmath_best_prefix_SI(self):
        """bitmath.best_prefix return a Kilobyte for 1024"""
        result = bitmath.best_prefix(1024, system=bitmath.SI)
        self.assertIs(type(result), bitmath.kB)

    def test_bitmath_best_prefix_SI_yotta(self):
        """bitmath.best_prefix return a yottabyte for a huge number of bytes"""
        result = bitmath.best_prefix(1000000000000000000000001, system=bitmath.SI)
        self.assertIs(type(result), bitmath.YB)
