# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# The MIT License (MIT)
#
# Copyright © 2026 Tim Case <timbielawa@gmail.com>
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
Tests for bitmath.query_capacity()
"""

import os
import pathlib
from unittest import skipUnless

import bitmath
from bitmath import Bitmath, Byte, Capacity

from . import TestCase


class TestQueryCapacity(TestCase):
    @skipUnless(os.name == 'posix', 'POSIX only')
    def test_query_capacity_posix_root(self):
        """query_capacity('/') returns a valid Capacity on POSIX"""
        result = bitmath.query_capacity("/")
        self.assertIsInstance(result, Capacity)
        self.assertIsInstance(result.total, Bitmath)
        self.assertIsInstance(result.used, Bitmath)
        self.assertIsInstance(result.free, Bitmath)
        self.assertGreater(result.total.bytes, 0)
        self.assertLessEqual(result.used.bytes + result.free.bytes, result.total.bytes)

    @skipUnless(os.name == 'posix', 'POSIX only')
    def test_query_capacity_posix_cwd(self):
        """query_capacity('.') returns valid Capacity for cwd on POSIX"""
        result = bitmath.query_capacity(".")
        self.assertIsInstance(result, Capacity)
        self.assertGreater(result.total.bytes, 0)
        self.assertLessEqual(result.used.bytes + result.free.bytes, result.total.bytes)

    @skipUnless(os.name == 'posix', 'POSIX only')
    def test_query_capacity_tuple_unpacking(self):
        """query_capacity result supports tuple unpacking"""
        t, u, f = bitmath.query_capacity("/")
        self.assertIsInstance(t, Bitmath)
        self.assertIsInstance(u, Bitmath)
        self.assertIsInstance(f, Bitmath)

    @skipUnless(os.name == 'posix', 'POSIX only')
    def test_query_capacity_bestprefix_false_returns_bytes(self):
        """bestprefix=False returns raw Byte instances"""
        result = bitmath.query_capacity("/", bestprefix=False)
        self.assertIs(type(result.total), Byte)
        self.assertIs(type(result.used), Byte)
        self.assertIs(type(result.free), Byte)

    @skipUnless(os.name == 'posix', 'POSIX only')
    def test_query_capacity_bestprefix_true_preserves_bytes(self):
        """bestprefix=True preserves underlying byte counts"""
        raw = bitmath.query_capacity("/", bestprefix=False)
        pretty = bitmath.query_capacity("/")
        self.assertEqual(raw.total.bytes, pretty.total.bytes)
        self.assertEqual(raw.used.bytes, pretty.used.bytes)
        self.assertEqual(raw.free.bytes, pretty.free.bytes)

    @skipUnless(os.name == 'posix', 'POSIX only')
    def test_query_capacity_system_nist_vs_si(self):
        """system kwarg switches between NIST (GiB) and SI (GB) prefixes"""
        nist = bitmath.query_capacity("/", system=bitmath.NIST)
        si = bitmath.query_capacity("/", system=bitmath.SI)
        # Same underlying bytes, different display units.
        self.assertEqual(nist.total.bytes, si.total.bytes)
        # NIST units end in 'iB' (e.g. GiB, MiB); SI units do not.
        # On a sufficiently large volume these will differ in unit class.
        if nist.total.bytes >= 1000:
            self.assertTrue(nist.total.unit.endswith('iB') or nist.total.unit == 'Byte')
            self.assertFalse(si.total.unit.endswith('iB'))

    @skipUnless(os.name == 'posix', 'POSIX only')
    def test_query_capacity_pathlike_input(self):
        """query_capacity accepts pathlib.Path input"""
        result = bitmath.query_capacity(pathlib.Path("/"))
        self.assertIsInstance(result, Capacity)
        self.assertGreater(result.total.bytes, 0)

    def test_query_capacity_nonexistent_path_raises(self):
        """query_capacity raises FileNotFoundError for a path that does not exist"""
        with self.assertRaises((FileNotFoundError, OSError)):
            bitmath.query_capacity("/nonexistent/path/that/should/not/exist/xyzzy")

    @skipUnless(os.name == 'nt', 'Windows only')
    def test_query_capacity_windows_drive_letter_normalization(self):
        """query_capacity normalizes bare drive letters on Windows"""
        c_bare = bitmath.query_capacity("C")
        c_colon = bitmath.query_capacity("C:")
        c_backslash = bitmath.query_capacity("C:\\")
        c_lower = bitmath.query_capacity("c")
        self.assertEqual(c_bare, c_colon)
        self.assertEqual(c_bare, c_backslash)
        self.assertEqual(c_bare, c_lower)

    @skipUnless(os.name == 'nt', 'Windows only')
    def test_query_capacity_windows_pathlike_drive_letter(self):
        """query_capacity normalizes a pathlib drive-letter input on Windows"""
        result = bitmath.query_capacity(pathlib.PureWindowsPath("C:"))
        self.assertIsInstance(result, Capacity)
        self.assertGreater(result.total.bytes, 0)
