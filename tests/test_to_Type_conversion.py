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
Test to verify the bitmath.Type.to_Type() conversions work
"""

from . import TestCase
import bitmath


class TestToTypeConversion(TestCase):
    def setUp(self):
        self.bit = bitmath.Bit(1)
        self.byte = bitmath.Byte(1)
        # NIST units
        self.kib = bitmath.KiB(1)
        self.mib = bitmath.MiB(1)
        self.gib = bitmath.GiB(1)
        self.tib = bitmath.TiB(1)
        self.pib = bitmath.PiB(1)
        self.eib = bitmath.EiB(1)

        # SI units
        self.kb = bitmath.kB(1)
        self.mb = bitmath.MB(1)
        self.gb = bitmath.GB(1)
        self.tb = bitmath.TB(1)
        self.pb = bitmath.PB(1)
        self.eb = bitmath.EB(1)
        self.zb = bitmath.ZB(1)
        self.yb = bitmath.YB(1)

    def test_to_same_unit(self):
        """bitmath type converted to the same unit is properly converted"""
        to_kib = self.kib.to_KiB()
        self.assertIs(type(to_kib), bitmath.KiB)
        self.assertIs(type(self.kib.KiB), bitmath.KiB)

    def test_from_other(self):
        """MiB object from_other object"""
        mib_from_kib = bitmath.MiB.from_other(bitmath.KiB(1))
        self.assertIs(type(mib_from_kib), bitmath.MiB)

    ##################################################################
    # to b's
    def test_to_Bit(self):
        """Convert to Bit"""
        self.assertIs(type(self.kb.to_Bit()), bitmath.Bit)
        self.assertIs(type(self.kb.Bit), bitmath.Bit)

    def test_to_Byte(self):
        """Convert to Byte"""
        self.assertIs(type(self.kb.to_Byte()), bitmath.Byte)
        self.assertIs(type(self.kb.Byte), bitmath.Byte)

    ##################################################################
    # to k's
    def test_to_KiB(self):
        """Convert to KiB"""
        to_kib = self.mib.to_KiB()
        self.assertIs(type(to_kib), bitmath.KiB)
        self.assertIs(type(self.mib.KiB), bitmath.KiB)

    def test_to_Kib(self):
        """Convert to Kib"""
        to_kib = self.mib.to_Kib()
        self.assertIs(type(to_kib), bitmath.Kib)
        self.assertIs(type(self.mib.Kib), bitmath.Kib)

    def test_to_kb(self):
        """Convert to kb"""
        to_kb = self.mib.to_kb()
        self.assertIs(type(to_kb), bitmath.kb)
        self.assertIs(type(self.mib.kb), bitmath.kb)

    ##################################################################
    # to m's
    def test_to_MiB(self):
        """Convert a bitmath GiB into a MiB"""
        to_mib = self.gib.to_MiB()
        self.assertIs(type(to_mib), bitmath.MiB)
        self.assertIs(type(self.gib.MiB), bitmath.MiB)

    def test_to_Mib(self):
        """Convert a bitmath GiB into a Mib"""
        to_mib = self.gib.to_Mib()
        self.assertIs(type(to_mib), bitmath.Mib)
        self.assertIs(type(self.gib.Mib), bitmath.Mib)

    def test_to_MB(self):
        """Convert a bitmath GiB into a MB"""
        to_mb = self.gib.to_MB()
        self.assertIs(type(to_mb), bitmath.MB)
        self.assertIs(type(self.gib.MB), bitmath.MB)

    def test_to_Mb(self):
        """Convert a bitmath GiB into a Mb"""
        to_mb = self.gib.to_Mb()
        self.assertIs(type(to_mb), bitmath.Mb)
        self.assertIs(type(self.gib.Mb), bitmath.Mb)

    ##################################################################
    # to g's
    def test_to_GiB(self):
        """Convert a bitmath TiB into a GiB"""
        to_gib = self.tib.to_GiB()
        self.assertIs(type(to_gib), bitmath.GiB)
        self.assertIs(type(self.tib.GiB), bitmath.GiB)

    def test_to_Gib(self):
        """Convert a bitmath GiB into a Gib"""
        to_gib = self.gib.to_Gib()
        self.assertIs(type(to_gib), bitmath.Gib)
        self.assertIs(type(self.tib.Gib), bitmath.Gib)

    def test_to_GB(self):
        """Convert a bitmath GiB into a GB"""
        to_gb = self.gib.to_GB()
        self.assertIs(type(to_gb), bitmath.GB)
        self.assertIs(type(self.tib.GB), bitmath.GB)

    def test_to_Gb(self):
        """Convert a bitmath GiB into a Gb"""
        to_gb = self.gib.to_Gb()
        self.assertIs(type(to_gb), bitmath.Gb)
        self.assertIs(type(self.tib.Gb), bitmath.Gb)

    ##################################################################
    # to t's
    def test_to_TiB(self):
        """Convert a bitmath PiB into a TiB"""
        to_tib = self.pib.to_TiB()
        self.assertIs(type(to_tib), bitmath.TiB)
        self.assertIs(type(self.pib.TiB), bitmath.TiB)

    def test_to_Tib(self):
        """Convert a bitmath GiB into a Tib"""
        to_tib = self.gib.to_Tib()
        self.assertIs(type(to_tib), bitmath.Tib)
        self.assertIs(type(self.pib.Tib), bitmath.Tib)

    def test_to_TB(self):
        """Convert a bitmath GiB into a TB"""
        to_tb = self.gib.to_TB()
        self.assertIs(type(to_tb), bitmath.TB)
        self.assertIs(type(self.pib.TB), bitmath.TB)

    def test_to_Tb(self):
        """Convert a bitmath GiB into a Tb"""
        to_tb = self.gib.to_Tb()
        self.assertIs(type(to_tb), bitmath.Tb)
        self.assertIs(type(self.pib.Tb), bitmath.Tb)

    ##################################################################
    # to p's
    def test_to_PiB(self):
        """Convert a bitmath TiB into a PiB"""
        to_pib = self.tib.to_PiB()
        self.assertIs(type(to_pib), bitmath.PiB)
        self.assertIs(type(self.tib.PiB), bitmath.PiB)

    def test_to_Pib(self):
        """Convert a bitmath GiB into a PiB"""
        to_pib = self.gib.to_Pib()
        self.assertIs(type(to_pib), bitmath.Pib)
        self.assertIs(type(self.gib.Pib), bitmath.Pib)

    def test_to_PB(self):
        """Convert a bitmath GiB into a PB"""
        to_pb = self.gib.to_PB()
        self.assertIs(type(to_pb), bitmath.PB)
        self.assertIs(type(self.gib.PB), bitmath.PB)

    def test_to_Pb(self):
        """Convert a bitmath GiB into a Pb"""
        to_pb = self.gib.to_Pb()
        self.assertIs(type(to_pb), bitmath.Pb)
        self.assertIs(type(self.gib.Pb), bitmath.Pb)

    ##################################################################
    # to e's
    def test_to_EiB(self):
        """Convert a bitmath PiB into a EiB"""
        to_eib = self.pib.to_EiB()
        self.assertIs(type(to_eib), bitmath.EiB)
        self.assertIs(type(self.pib.EiB), bitmath.EiB)

    def test_to_Eib(self):
        """Convert a bitmath GiB into a Eib"""
        to_eib = self.gib.to_Eib()
        self.assertIs(type(to_eib), bitmath.Eib)
        self.assertIs(type(self.pib.Eib), bitmath.Eib)

    def test_to_EB(self):
        """Convert a bitmath GiB into a EB"""
        to_eb = self.gib.to_EB()
        self.assertIs(type(to_eb), bitmath.EB)
        self.assertIs(type(self.pib.EB), bitmath.EB)

    def test_to_Eb(self):
        """Convert a bitmath GiB into a Eb"""
        to_eb = self.gib.to_Eb()
        self.assertIs(type(to_eb), bitmath.Eb)
        self.assertIs(type(self.pib.Eb), bitmath.Eb)

    ##################################################################
    # to z's
    def test_to_ZB(self):
        """Convert a bitmath GiB into a ZB"""
        to_zb = self.gib.to_ZB()
        self.assertIs(type(to_zb), bitmath.ZB)
        self.assertIs(type(self.pib.ZB), bitmath.ZB)

    def test_to_Zb(self):
        """Convert a bitmath GiB into a Zb"""
        to_zb = self.gib.to_Zb()
        self.assertIs(type(to_zb), bitmath.Zb)
        self.assertIs(type(self.pib.Zb), bitmath.Zb)

    ##################################################################
    # to y's
    def test_to_YB(self):
        """Convert a bitmath GiB into a YB"""
        to_yb = self.gib.to_YB()
        self.assertIs(type(to_yb), bitmath.YB)
        self.assertIs(type(self.pib.YB), bitmath.YB)

    def test_to_Yb(self):
        """Convert a bitmath GiB into a Yb"""
        to_yb = self.gib.to_Yb()
        self.assertIs(type(to_yb), bitmath.Yb)
        self.assertIs(type(self.pib.Yb), bitmath.Yb)

    ##################################################################
    # to other stuff
    def test_to_mib_from_bit(self):
        """Convert a bitmath Bit into a MiB"""
        to_mib = self.bit.to_MiB()
        self.assertIs(type(to_mib), bitmath.MiB)

    def test_converted_up_bitmath_value_equivalency(self):
        """Converted up type has an equivalent value to the original"""
        # Take a KiB, make a MiB from it. Test their equality
        to_mib = self.kib.to_MiB()
        self.assertEqual(self.kib, to_mib)

        # Two tests, to be "thorough"
        to_gib = self.mib.to_GiB()
        self.assertEqual(self.mib, to_gib)

    def test_converted_down_bitmath_value_equivalency(self):
        """Converted down type has an equivalent value to the original"""
        # Take a MiB, make a KiB from it. Test their equality
        to_kib = self.mib.to_KiB()
        self.assertEqual(to_kib, self.mib)

    def test_convert_nist_to_si(self):
        """Convert an NIST unit into an SI unit"""
        kb_from_kib = self.kib.to_kB()
        self.assertIs(type(kb_from_kib), bitmath.kB)

    def test_convert_si_to_nist(self):
        """Convert an SI unit into an NIST unit"""
        kib_from_kb = self.kb.to_KiB()
        self.assertIs(type(kib_from_kb), bitmath.KiB)

    ##################################################################
    # Naughty bad bad test cases
    def test_from_other_bad_input(self):
        """from_other raises if "other" isn't a bitmath instance"""
        with self.assertRaises(ValueError):
            bitmath.Byte.from_other(str("not a bitmath instance!"))
