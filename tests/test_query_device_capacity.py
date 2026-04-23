# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
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
Test reading block device capacities
"""

from . import TestCase
import bitmath
from unittest import mock
import struct
from contextlib import ExitStack, contextmanager


@contextmanager
def nested(*contexts):
    with ExitStack() as stack:
        yield tuple(stack.enter_context(c) for c in contexts)


device_file_no = mock.Mock(return_value=4)
device = mock.MagicMock('file')
device.fileno = device_file_no
device.name = "/dev/sda"

non_device_file = mock.MagicMock('file')
non_device_file.name = "/home/"

windows_device = mock.MagicMock('file')
windows_device.fileno = mock.Mock(return_value=4)
windows_device.name = r'\\.\PhysicalDrive0'

windows_non_device = mock.MagicMock('file')
windows_non_device.name = r'C:\somefile.txt'


class TestQueryDeviceCapacity(TestCase):
    def test_query_device_capacity_linux_everything_is_wonderful(self):
        """query device capacity works on a happy Linux host"""
        with nested(
            mock.patch('os.stat'),
            mock.patch('stat.S_ISBLK'),
            mock.patch('platform.system'),
            mock.patch('fcntl.ioctl'),
        ) as (os_stat, stat_is_block, plat_system, ioctl):
            os_stat.return_value = mock.Mock(st_mode=25008)
            stat_is_block.return_value = True
            plat_system.return_value = 'Linux'
            ioctl.return_value = struct.pack('L', 244140625)
            # = 'QJ\x8d\x0e\x00\x00\x00\x00'
            # = 244140625 ~= 244.140625 MB (in SI)
            bytes = bitmath.query_device_capacity(device)
            self.assertEqual(bytes, 244140625)
            self.assertEqual(ioctl.call_count, 1)
            ioctl.assert_called_once_with(4, 0x80081272, struct.calcsize('L'))

    def test_query_device_capacity_mac_everything_is_wonderful(self):
        """query device capacity works on a happy Mac OS X host"""
        with nested(
            mock.patch('os.stat'),
            mock.patch('stat.S_ISBLK'),
            mock.patch('platform.system'),
            mock.patch('fcntl.ioctl'),
        ) as (os_stat, stat_is_block, plat_system, ioctl):
            # These are the struct.pack() equivalents of 244140625
            # (type: u64) and 4096 (type: u32). Multiplied together
            # they equal the number of bytes in 1 TB.
            returns = [
                struct.pack('L', 244140625),  # 'QJ\x8d\x0e\x00\x00\x00\x00'
                struct.pack('I', 4096)  # , '\x00\x10\x00\x00'
            ]

            def side_effect(*args, **kwargs):
                return returns.pop(0)

            os_stat.return_value = mock.Mock(st_mode=25008)
            stat_is_block.return_value = True
            plat_system.return_value = 'Darwin'
            ioctl.side_effect = side_effect

            bytes = bitmath.query_device_capacity(device)
            # The result should be 1 TB
            self.assertEqual(bytes, 1000000000000)
            self.assertEqual(ioctl.call_count, 2)

    def test_query_device_capacity_device_not_block(self):
        """query device capacity aborts if a non-block-device is provided"""
        with nested(
            mock.patch('os.stat'),
            mock.patch('stat.S_ISBLK'),
            mock.patch('fcntl.ioctl'),
        ) as (os_stat, stat_is_block, ioctl):
            os_stat.return_value = mock.Mock(st_mode=33204)
            # Force ISBLK to reject the input 'device'
            stat_is_block.return_value = False

            with self.assertRaises(ValueError):
                bitmath.query_device_capacity(non_device_file)

            self.assertEqual(ioctl.call_count, 0)

    def test_query_device_capacity_windows_everything_is_wonderful(self):
        """query device capacity works on a happy Windows host"""
        expected_bytes = 1_000_000_000_000  # 1 TB

        with mock.patch('bitmath._query_device_capacity_windows', return_value=expected_bytes):
            with mock.patch('bitmath.os.name', 'nt'):
                result = bitmath.query_device_capacity(windows_device)

        self.assertEqual(result, bitmath.Byte(expected_bytes))

    def test_query_device_capacity_windows_non_device_fails(self):
        """query device capacity rejects a non-device path on Windows"""
        with mock.patch('bitmath.os.name', 'nt'):
            with self.assertRaises(ValueError):
                bitmath.query_device_capacity(windows_non_device)

    def test_query_device_capacity_unsupported_platform_fails(self):
        """query device capacity fails on an unsupported platform"""
        # Derive a value that is guaranteed not to be in SUPPORTED_PLATFORMS.
        unsupported = next(
            p for p in ('os2', 'java', 'riscos', 'ce')
            if p not in bitmath.SUPPORTED_PLATFORMS
        )
        with mock.patch('bitmath.os.name', unsupported):
            with self.assertRaises(NotImplementedError):
                bitmath.query_device_capacity(device)
