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
import ctypes as real_ctypes
import os
import types
from unittest import mock, skipUnless
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
    @skipUnless(os.name == 'posix', 'fcntl is POSIX only')
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
            ioctl.assert_called_once_with(4, 0x80081272, b'\x00' * struct.calcsize('L'))

    def test_query_device_capacity_macos_raises(self):
        """query_device_capacity raises NotImplementedError on macOS (SIP restriction)"""
        with mock.patch('bitmath.os.name', 'posix'):
            with mock.patch('bitmath.platform.system', return_value='Darwin'):
                with self.assertRaises(NotImplementedError) as ctx:
                    bitmath.query_device_capacity(device)
        self.assertIn('SIP', str(ctx.exception))

    @skipUnless(os.name == 'posix', 'fcntl is POSIX only')
    def test_query_device_capacity_device_not_block(self):
        """query device capacity aborts if a non-block-device is provided"""
        with nested(
            mock.patch('os.stat'),
            mock.patch('stat.S_ISBLK'),
            mock.patch('platform.system'),
            mock.patch('fcntl.ioctl'),
        ) as (os_stat, stat_is_block, plat_system, ioctl):
            os_stat.return_value = mock.Mock(st_mode=33204)
            # Force ISBLK to reject the input 'device'
            stat_is_block.return_value = False
            plat_system.return_value = 'Linux'

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


class TestQueryDeviceCapacityWindowsBody(TestCase):
    """Mock-based tests for _query_device_capacity_windows body.

    Run on all platforms by injecting ctypes and msvcrt into the bitmath
    namespace via mock.patch(..., create=True).
    """

    def _make_mock_ctypes(self):
        mc = types.SimpleNamespace(
            Structure=real_ctypes.Structure,
            c_longlong=real_ctypes.c_longlong,
            c_uint=real_ctypes.c_uint,
            c_ulong=real_ctypes.c_ulong,
            c_byte=real_ctypes.c_byte,
            byref=real_ctypes.byref,
            sizeof=real_ctypes.sizeof,
            wintypes=types.SimpleNamespace(DWORD=real_ctypes.c_ulong),
            windll=mock.MagicMock(),
        )
        mc.windll.kernel32.DeviceIoControl.return_value = 1
        return mc

    def _make_mock_msvcrt(self):
        return types.SimpleNamespace(get_osfhandle=mock.Mock(return_value=999))

    def _make_windows_device(self):
        fd = mock.MagicMock()
        fd.name = r'\\.\PhysicalDrive0'
        fd.fileno.return_value = 4
        return fd

    def test_windows_body_success(self):
        """_query_device_capacity_windows succeeds via mocked ctypes and msvcrt"""
        mock_ctypes = self._make_mock_ctypes()
        mock_msvcrt = self._make_mock_msvcrt()
        device_fd = self._make_windows_device()

        with mock.patch('bitmath.ctypes', mock_ctypes, create=True):
            with mock.patch('bitmath.msvcrt', mock_msvcrt, create=True):
                result = bitmath._query_device_capacity_windows(device_fd)

        # DiskSize is 0 by default — mock DeviceIoControl does not fill the struct
        self.assertEqual(result, 0)
        mock_msvcrt.get_osfhandle.assert_called_once_with(4)
        mock_ctypes.windll.kernel32.DeviceIoControl.assert_called_once()

    def test_windows_body_ioctl_failure_raises_oserror(self):
        """_query_device_capacity_windows raises OSError when DeviceIoControl fails"""
        mock_ctypes = self._make_mock_ctypes()
        mock_ctypes.windll.kernel32.DeviceIoControl.return_value = 0
        mock_ctypes.windll.kernel32.GetLastError.return_value = 5
        mock_msvcrt = self._make_mock_msvcrt()
        device_fd = self._make_windows_device()

        with mock.patch('bitmath.ctypes', mock_ctypes, create=True):
            with mock.patch('bitmath.msvcrt', mock_msvcrt, create=True):
                with self.assertRaises(OSError):
                    bitmath._query_device_capacity_windows(device_fd)
