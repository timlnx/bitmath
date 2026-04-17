# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright © 2014 Tim Bielawa <timbielawa@gmail.com>
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
Test the progressbar 'FileTransferSpeed' integration
"""

from . import TestCase
import bitmath
from bitmath.integrations.bmprogressbar import BitmathFileTransferSpeed
try:
    from unittest import mock
except ImportError:
    import mock
import progressbar


class TestProgressbar(TestCase):
    def setUp(self):
        """Needful for the tests"""
        self.widget_NIST = BitmathFileTransferSpeed(system=bitmath.NIST)
        self.widget_SI = BitmathFileTransferSpeed(system=bitmath.SI)
        self.widget_formatted = BitmathFileTransferSpeed(format="{value:.6f} {unit_plural} per second")

    def test_FileTransferSpeed_0_seconds(self):
        """Widget renders 0 correctly when no seconds have elapsed"""
        pbar = mock.MagicMock(progressbar.ProgressBar)
        pbar.seconds_elapsed = 0
        pbar.currval = 0
        update = self.widget_NIST.update(pbar)
        self.assertEqual(update, '0.00 Byte/s')

    def test_FileTransferSpeed_1_seconds_Bytes(self):
        """Widget renders a non-zero rate after time has elapsed in Bytes"""
        pbar = mock.MagicMock(progressbar.ProgressBar)
        pbar.seconds_elapsed = 1
        pbar.currval = 512
        update = self.widget_NIST.update(pbar)
        self.assertEqual(update, '512.00 Byte/s')

    def test_FileTransferSpeed_10_seconds_MiB(self):
        """Widget renders a rate after time has elapsed in MiB/s"""
        pbar = mock.MagicMock(progressbar.ProgressBar)
        pbar.seconds_elapsed = 10
        # Let's say we've downloaded 512 MiB in that time (we need
        # that value in Bytes, though)
        pbar.currval = bitmath.MiB(512).bytes
        update = self.widget_NIST.update(pbar)
        # 512 MiB in 10 seconds is equal to a rate of 51.20 MiB/s
        self.assertEqual(update, '51.20 MiB/s')

    def test_FileTransferSpeed_10_seconds_MB(self):
        """Widget renders a rate after time has elapsed in MB/s"""
        pbar = mock.MagicMock(progressbar.ProgressBar)
        pbar.seconds_elapsed = 10
        # Let's say we've downloaded 512 MB in that time (we need that
        # value in Bytes, though)
        pbar.currval = bitmath.MB(512).bytes
        update = self.widget_SI.update(pbar)
        # 512 MB in 10 seconds is equal to a rate of 51.20 MB/s
        self.assertEqual(update, '51.20 MB/s')

    def test_FileTransferSpeed_custom_format(self):
        """Widget renders a custom format string"""
        pbar = mock.MagicMock(progressbar.ProgressBar)
        pbar.seconds_elapsed = 10
        pbar.currval = 10240
        update = self.widget_formatted.update(pbar)
        self.assertEqual(update, '1.000000 KiBs per second')
