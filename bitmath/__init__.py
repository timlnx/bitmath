# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# The MIT License (MIT)
#
# Copyright © 2014-2016 Tim Case <timbielawa@gmail.com>
# See GitHub Contributors Graph for more information
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sub-license, and/or sell copies of the Software,
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
# pylint: disable=bad-continuation,missing-docstring,invalid-name,line-too-long

"""Reference material:
The bitmath homepage is located at:
* http://bitmath.readthedocs.io/en/latest/

Prefixes for binary multiples:
http://physics.nist.gov/cuu/Units/binary.html

decimal and binary prefixes:
man 7 units (from the Linux Documentation Project 'man-pages' package)


* If you *NEED* to skip a statement because of something untestable:

      # pragma: no cover
"""

from __future__ import annotations

import argparse
import contextlib
import fnmatch
import math
import numbers
import os
import os.path
import platform
import sys
import threading

from collections.abc import Generator, Iterable, Iterator
from typing import IO, Any

# For device capacity reading in query_device_capacity().
if os.name == 'posix':
    import stat
    import fcntl
    import struct
elif os.name == 'nt':
    import ctypes
    import ctypes.wintypes
    import msvcrt

#: Platforms where :func:`query_device_capacity` is supported.
#: Corresponds to possible values of :data:`os.name`.
SUPPORTED_PLATFORMS = frozenset({'posix', 'nt'})

__all__ = ['Bit', 'Byte', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB',
           'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB', 'Kib',
           'Mib', 'Gib', 'Tib', 'Pib', 'Eib', 'Zib', 'Yib', 'kb', 'Mb', 'Gb', 'Tb',
           'Pb', 'Eb', 'Zb', 'Yb', 'getsize', 'listdir', 'format',
           'format_string', 'format_plural', 'parse_string', 'parse_string_unsafe',
           'sum', 'ALL_UNIT_TYPES', 'NIST', 'NIST_PREFIXES', 'NIST_STEPS',
           'SI', 'SI_PREFIXES', 'SI_STEPS']

#: A list of all the valid prefix unit types. Mostly for reference,
#: also used by the CLI tool as valid types
ALL_UNIT_TYPES = ['Bit', 'Byte', 'kb', 'kB', 'Mb', 'MB', 'Gb', 'GB', 'Tb',
                  'TB', 'Pb', 'PB', 'Eb', 'EB', 'Zb', 'ZB', 'Yb',
                  'YB', 'Kib', 'KiB', 'Mib', 'MiB', 'Gib', 'GiB',
                  'Tib', 'TiB', 'Pib', 'PiB', 'Eib', 'EiB', 'Zib', 'ZiB',
                  'Yib', 'YiB']

# #####################################################################
# Set up our module variables/constants

###################################
# Internal:

# Console repr(), ex: MiB(13.37), or kB(42.0)
_FORMAT_REPR = '{unit_singular}({value})'

# ##################################
# Exposed:

#: Constants for referring to NIST prefix system
NIST = int(2)

#: Constants for referring to SI prefix system
SI = int(10)

# ##################################

#: All of the SI prefixes
SI_PREFIXES = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']

#: Byte values represented by each SI prefix unit
SI_STEPS = {
    'Bit': 1 / 8.0,
    'Byte': 1,
    'k': 1000,
    'M': 1000000,
    'G': 1000000000,
    'T': 1000000000000,
    'P': 1000000000000000,
    'E': 1000000000000000000,
    'Z': 1000000000000000000000,
    'Y': 1000000000000000000000000
}


#: All of the NIST prefixes
NIST_PREFIXES = ['Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']

#: Byte values represented by each NIST prefix unit
NIST_STEPS = {
    'Bit': 1 / 8.0,
    'Byte': 1,
    'Ki': 1024,
    'Mi': 1048576,
    'Gi': 1073741824,
    'Ti': 1099511627776,
    'Pi': 1125899906842624,
    'Ei': 1152921504606846976,
    'Zi': 1180591620717411303424,
    'Yi': 1208925819614629174706176
}

#: String representation, ex: ``13.37 MiB``, or ``42.0 kB``
format_string = "{value} {unit}"

#: Pluralization behavior
format_plural = False

# Thread-local storage for context manager overrides. When a thread is inside
# a bitmath.format() context, these shadow the module globals above for that
# thread only — other threads are unaffected.
_thread_local = threading.local()
_FMT_SENTINEL = object()  # distinguishes "not set" from any real value


def _get_format_string():
    return getattr(_thread_local, 'format_string', format_string)


def _get_format_plural():
    return getattr(_thread_local, 'format_plural', format_plural)


def _get_bestprefix():
    return getattr(_thread_local, 'bestprefix', False)


def capitalize_first(s: str) -> str:
    """Capitalize ONLY the first letter of the input `s`

* returns a copy of input `s` with the first letter capitalized
    """
    pfx = s[0].upper()
    _s = s[1:]
    return pfx + _s


######################################################################
# Base class for everything else
class Bitmath:
    """The base class for all the other prefix classes"""

    # All the allowed input types
    valid_types: tuple[type, ...] = (int, float)

    def __init__(self, value=0, bytes=None, bits=None):
        """Instantiate with `value` by the unit, in plain bytes, or
bits. Don't supply more than one keyword.

default behavior: initialize with value of 0
only setting value: assert bytes is None and bits is None
only setting bytes: assert value == 0 and bits is None
only setting bits: assert value == 0 and bytes is None
        """
        _raise = False
        if (value == 0) and (bytes is None) and (bits is None):
            pass
        # Setting by bytes
        elif bytes is not None:
            if (value == 0) and (bits is None):
                pass
            else:
                _raise = True
        # setting by bits
        elif bits is not None:
            if (value == 0) and (bytes is None):
                pass
            else:
                _raise = True

        if _raise:
            raise ValueError("Only one parameter of: value, bytes, or bits is allowed")

        self._do_setup()
        if bytes:
            # We were provided with the fundamental base unit, no need
            # to normalize
            self._byte_value = bytes
            self._bit_value = bytes * 8.0
        elif bits:
            # We were *ALMOST* given the fundamental base
            # unit. Translate it into the fundamental unit then
            # normalize.
            self._byte_value = bits / 8.0
            self._bit_value = bits
        else:
            # We were given a value representative of this *prefix
            # unit*. We need to normalize it into the number of bytes
            # it represents.
            self._norm(value)

        # We have the fundamental unit figured out. Set the 'pretty' unit
        self._set_prefix_value()

    def _set_prefix_value(self) -> None:
        self.prefix_value = self._to_prefix_value(self._byte_value)

    def _to_prefix_value(self, value: float) -> float:
        """Return the number of bits/bytes as they would look like if we
converted *to* this unit"""
        return value / float(self._unit_value)

    def _setup(self) -> tuple:
        raise NotImplementedError("The base 'bitmath.Bitmath' class can not be used directly")

    def _do_setup(self) -> None:
        """Setup basic parameters for this class.

`base` is the numeric base which when raised to `power` is equivalent
to 1 unit of the corresponding prefix. I.e., base=2, power=10
represents 2^10, which is the NIST Binary Prefix for 1 Kibibyte.

Likewise, for the SI prefix classes `base` will be 10, and the `power`
for the Kilobyte is 3.
"""
        (self._base, self._power, self._name_singular, self._name_plural) = self._setup()
        self._unit_value = self._base ** self._power

    def _norm(self, value: int | float) -> None:
        """Normalize the input value into the fundamental unit for this prefix
type.

   :param number value: The input value to be normalized
   :raises ValueError: if the input value is not a type of real number
"""
        if isinstance(value, self.valid_types):
            self._byte_value = float(value) * self._unit_value
            self._bit_value = self._byte_value * 8.0
        else:
            raise ValueError(
                f"Initialization value '{value}' is of an invalid type: {type(value)}. "
                f"Must be one of {', '.join(str(x) for x in self.valid_types)}"
            )

    ##################################################################
    # Properties

    #: The mathematical base of an instance
    base = property(lambda s: s._base,
                    doc="The mathematical base of the unit of the instance (this will be 2 or 10)")

    binary = property(lambda s: bin(int(s.bits)),
                      doc="""The binary representation of an instance in binary 1s and 0s. Note
that for very large numbers this will mean a lot of 1s and 0s. For
example, GiB(100) would be represented in Python as::

    0b1100100000000000000000000000000000000000
That leading ``0b`` is normal. That's how Python represents binary.
""")

    #: Alias for :attr:`binary`
    bin = property(lambda s: s.binary, doc="Alias for the 'binary' property")

    #: The number of bits in an instance
    bits = property(lambda s: s._bit_value, doc="The number of bits in an instance")

    #: The number of bytes in an instance
    bytes = property(lambda s: s._byte_value, doc="The number of bytes in an instance")

    #: The mathematical power of an instance
    power = property(lambda s: s._power, doc="The mathematical power of an instance")

    @property
    def system(self):
        """The system of units used to measure an instance"""
        if self._base == 2:
            return "NIST"
        elif self._base == 10:
            return "SI"
        else:
            # I don't expect to ever encounter this logic branch, but
            # hey, it's better to have extra test coverage than
            # insufficient test coverage.
            raise ValueError(f"Instances mathematical base is an unsupported value: {self._base}")

    @property
    def unit(self):
        """The string that is this instances prefix unit name in agreement
with this instance value (singular or plural). Following the
convention that only 1 is singular. This will always be the singular
form when :attr:`bitmath.format_plural` is ``False`` (default value).

For example:

   >>> KiB(1).unit == 'KiB'
   >>> Byte(0).unit == 'Bytes'
   >>> Byte(1).unit == 'Byte'
   >>> Byte(1.1).unit == 'Bytes'
   >>> Gb(2).unit == 'Gbs'
        """
        if self.prefix_value == 1:
            # If it's a '1', return it singular, no matter what
            return self._name_singular
        elif _get_format_plural():
            # Pluralization requested
            return self._name_plural
        else:
            # Pluralization NOT requested, and the value is not 1
            return self._name_singular

    @property
    def unit_plural(self):
        """The string that is an instances prefix unit name in the plural
form.

For example:

   >>> KiB(1).unit_plural == 'KiB'
   >>> Byte(1024).unit_plural == 'Bytes'
   >>> Gb(1).unit_plural == 'Gb'
        """
        return self._name_plural

    @property
    def unit_singular(self):
        """The string that is an instances prefix unit name in the singular
form.

For example:

   >>> KiB(1).unit_singular == 'KiB'
   >>> Byte(1024).unit == 'B'
   >>> Gb(1).unit_singular == 'Gb'
        """
        return self._name_singular

    #: The "prefix" value of an instance
    value = property(lambda s: s.prefix_value)

    @classmethod
    def from_other(cls, item):
        """Factory function to return instances of `item` converted into a new
instance of ``cls``. Because this is a class method, it may be called
from any bitmath class object without the need to explicitly
instantiate the class ahead of time.

*Implicit Parameter:*

* ``cls`` A bitmath class, implicitly set to the class of the
  instance object it is called on

*User Supplied Parameter:*

* ``item`` A :class:`bitmath.Bitmath` subclass instance

*Example:*

   >>> import bitmath
   >>> kib = bitmath.KiB.from_other(bitmath.MiB(1))
   >>> print(kib)
   KiB(1024.0)

        """
        if isinstance(item, Bitmath):
            return cls(bits=item.bits)
        else:
            raise ValueError(f"The provided items must be a valid bitmath class: {item.__class__}")

    ######################################################################
    # The following implement the Python datamodel customization methods
    #
    # Reference: https://docs.python.org/3/reference/datamodel.html#basic-customization

    def __repr__(self) -> str:
        """Representation of this object as you would expect to see in an
interpreter"""
        return self.format(_FORMAT_REPR)

    def __str__(self) -> str:
        """String representation of this object"""
        if _get_bestprefix():
            return self.best_prefix().format(_get_format_string())
        return self.format(_get_format_string())

    def __format__(self, fmt_spec: str) -> str:
        """Support Python's string formatting protocol.

When *fmt_spec* is empty, returns ``str(self)`` — the same as the
default string representation (e.g. ``"1.0 KiB"``).

When *fmt_spec* is a standard numeric format spec (e.g. ``".2f"``,
``">10.1f"``), it is applied to ``self.value`` only, returning the
formatted number without a unit suffix. The caller controls the
surrounding string::

    size = bitmath.MiB(2.847598437)
    f'size: {size:.1f} {size.unit}'   # -> 'size: 2.8 MiB'
    f'size: {size}'                    # -> 'size: 2.847598437 MiB'
        """
        if fmt_spec == '':
            return str(self)
        return self.value.__format__(fmt_spec)

    def format(self, fmt: str) -> str:
        """Return a representation of this instance formatted with user
supplied syntax"""
        _fmt_params = {
            'base': self.base,
            'bin': self.bin,
            'binary': self.binary,
            'bits': self.bits,
            'bytes': self.bytes,
            'power': self.power,
            'system': self.system,
            'unit': self.unit,
            'unit_plural': self.unit_plural,
            'unit_singular': self.unit_singular,
            'value': self.value
        }

        return fmt.format(**_fmt_params)

    ##################################################################
    # Guess the best human-readable prefix unit for representation
    ##################################################################

    def best_prefix(self, system=None):
        """Optional parameter, `system`, allows you to prefer NIST or SI in
the results. By default, the current system is used (Bit/Byte default
to NIST).

Logic discussion/notes:

Base-case, does it need converting?

If the instance is less than one Byte, return the instance as a Bit
instance.

Else, begin by recording the unit system the instance is defined
by. This determines which steps (NIST_STEPS/SI_STEPS) we iterate over.

If the instance is not already a ``Byte`` instance, convert it to one
for the purpose of the log calculation.

NIST units step up by powers of 1024, SI units step up by powers of
1000.

Take integer value of the log(base=STEP_POWER) of the instance's byte
value. E.g.:

    >>> int(math.log(Gb(100).bytes, 1000))
    3

This will return a value >= 0. The following determines the 'best
prefix unit' for representation:

* result == 0, best represented as a Byte (or Bit for Bit-family inputs)
* result >= len(SYSTEM_STEPS), best represented as an Exbi/Exabyte
* 0 < result < len(SYSTEM_STEPS), best represented as SYSTEM_PREFIXES[result-1]

Unit family is preserved: Bit-family instances (Bit, Kib, Mib, kb,
Mb, etc.) always return a Bit-family result. Byte-family instances
always return a Byte-family result.

.. versionchanged:: 2.0.0
   Bit-family instances now return Bit-family results. Previously,
   ``best_prefix()`` always returned a Byte-family unit regardless of
   the input type (e.g. ``Bit(30950093).best_prefix()`` returned
   ``MiB`` instead of ``Mib``). See GitHub issue #95.

        """

        # Use absolute value so we don't return Bit's for *everything*
        # less than Byte(1). From github issue #55
        if abs(self) < Byte(1):
            return Bit.from_other(self)
        else:
            if isinstance(self, Byte):
                _inst = self
            else:
                _inst = Byte.from_other(self)

        # Which table to consult? Was a preferred system provided?
        if system is None:
            # No preference. Use existing system
            if self.system == 'NIST':
                _STEPS = NIST_PREFIXES
                _BASE = 1024
            elif self.system == 'SI':
                _STEPS = SI_PREFIXES
                _BASE = 1000
            # Anything else would have raised by now
        else:
            # Preferred system provided.
            if system == NIST:
                _STEPS = NIST_PREFIXES
                _BASE = 1024
            elif system == SI:
                _STEPS = SI_PREFIXES
                _BASE = 1000
            else:
                raise ValueError("Invalid value given for 'system' parameter."
                                 " Must be one of NIST or SI")

        # Index of the string of the best prefix in the STEPS list
        _index = int(math.log(abs(_inst.bytes), _BASE))

        # Recall that the log() function returns >= 0. This doesn't
        # map to the STEPS list 1:1. That is to say, 0 is handled with
        # special care. So if the _index is 1, we actually want item 0
        # in the list.

        if _index == 0:
            # Below the first prefix threshold. Bit-family inputs return as
            # Bit to preserve family; Byte-family inputs return as Byte.
            if isinstance(self, Bit):
                return Bit.from_other(self)
            return _inst
        elif _index >= len(_STEPS):
            # This is a really big number. Use the biggest prefix we've got
            _best_prefix = _STEPS[-1]
        elif 0 < _index < len(_STEPS):
            # There is an appropriate prefix unit to represent this
            _best_prefix = _STEPS[_index - 1]

        # Preserve unit family: Bit-family -> 'to_Xib'/'to_Xb',
        # Byte-family -> 'to_XiB'/'to_XB'.
        if isinstance(self, Bit):
            _conversion_method = getattr(self, 'to_%sb' % _best_prefix)
        else:
            _conversion_method = getattr(self, 'to_%sB' % _best_prefix)

        return _conversion_method()

    ##################################################################

    def to_Bit(self):
        return Bit(self._bit_value)

    def to_Byte(self):
        return Byte(self._byte_value / float(NIST_STEPS['Byte']))

    # Properties
    Bit = property(lambda s: s.to_Bit())
    Byte = property(lambda s: s.to_Byte())

    ##################################################################

    def to_KiB(self):
        return KiB(bits=self._bit_value)

    def to_Kib(self):
        return Kib(bits=self._bit_value)

    def to_kB(self):
        return kB(bits=self._bit_value)

    def to_kb(self):
        return kb(bits=self._bit_value)

    # Properties
    KiB = property(lambda s: s.to_KiB())
    Kib = property(lambda s: s.to_Kib())
    kB = property(lambda s: s.to_kB())
    kb = property(lambda s: s.to_kb())

    ##################################################################

    def to_MiB(self):
        return MiB(bits=self._bit_value)

    def to_Mib(self):
        return Mib(bits=self._bit_value)

    def to_MB(self):
        return MB(bits=self._bit_value)

    def to_Mb(self):
        return Mb(bits=self._bit_value)

    # Properties
    MiB = property(lambda s: s.to_MiB())
    Mib = property(lambda s: s.to_Mib())
    MB = property(lambda s: s.to_MB())
    Mb = property(lambda s: s.to_Mb())

    ##################################################################

    def to_GiB(self):
        return GiB(bits=self._bit_value)

    def to_Gib(self):
        return Gib(bits=self._bit_value)

    def to_GB(self):
        return GB(bits=self._bit_value)

    def to_Gb(self):
        return Gb(bits=self._bit_value)

    # Properties
    GiB = property(lambda s: s.to_GiB())
    Gib = property(lambda s: s.to_Gib())
    GB = property(lambda s: s.to_GB())
    Gb = property(lambda s: s.to_Gb())

    ##################################################################

    def to_TiB(self):
        return TiB(bits=self._bit_value)

    def to_Tib(self):
        return Tib(bits=self._bit_value)

    def to_TB(self):
        return TB(bits=self._bit_value)

    def to_Tb(self):
        return Tb(bits=self._bit_value)

    # Properties
    TiB = property(lambda s: s.to_TiB())
    Tib = property(lambda s: s.to_Tib())
    TB = property(lambda s: s.to_TB())
    Tb = property(lambda s: s.to_Tb())

    ##################################################################

    def to_PiB(self):
        return PiB(bits=self._bit_value)

    def to_Pib(self):
        return Pib(bits=self._bit_value)

    def to_PB(self):
        return PB(bits=self._bit_value)

    def to_Pb(self):
        return Pb(bits=self._bit_value)

    # Properties
    PiB = property(lambda s: s.to_PiB())
    Pib = property(lambda s: s.to_Pib())
    PB = property(lambda s: s.to_PB())
    Pb = property(lambda s: s.to_Pb())

    ##################################################################

    def to_EiB(self):
        return EiB(bits=self._bit_value)

    def to_Eib(self):
        return Eib(bits=self._bit_value)

    def to_EB(self):
        return EB(bits=self._bit_value)

    def to_Eb(self):
        return Eb(bits=self._bit_value)

    # Properties
    EiB = property(lambda s: s.to_EiB())
    Eib = property(lambda s: s.to_Eib())
    EB = property(lambda s: s.to_EB())
    Eb = property(lambda s: s.to_Eb())

    ##################################################################

    def to_ZiB(self):
        return ZiB(bits=self._bit_value)

    def to_Zib(self):
        return Zib(bits=self._bit_value)

    def to_ZB(self):
        return ZB(bits=self._bit_value)

    def to_Zb(self):
        return Zb(bits=self._bit_value)

    ZiB = property(lambda s: s.to_ZiB())
    Zib = property(lambda s: s.to_Zib())
    ZB = property(lambda s: s.to_ZB())
    Zb = property(lambda s: s.to_Zb())

    ##################################################################

    def to_YiB(self):
        return YiB(bits=self._bit_value)

    def to_Yib(self):
        return Yib(bits=self._bit_value)

    def to_YB(self):
        return YB(bits=self._bit_value)

    def to_Yb(self):
        return Yb(bits=self._bit_value)

    YiB = property(lambda s: s.to_YiB())
    Yib = property(lambda s: s.to_Yib())
    YB = property(lambda s: s.to_YB())
    Yb = property(lambda s: s.to_Yb())

    ##################################################################
    # Rich comparison operations
    ##################################################################

    def __lt__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value < other
        else:
            return self._byte_value < other.bytes

    def __le__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value <= other
        else:
            return self._byte_value <= other.bytes

    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value == other
        else:
            return self._byte_value == other.bytes

    def __ne__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value != other
        else:
            return self._byte_value != other.bytes

    def __gt__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value > other
        else:
            return self._byte_value > other.bytes

    def __ge__(self, other):
        if isinstance(other, numbers.Number):
            return self.prefix_value >= other
        else:
            return self._byte_value >= other.bytes

    ##################################################################
    # Basic math operations
    ##################################################################

    # Reference: https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types

    """These methods are called to implement the binary arithmetic
operations (+, -, *, //, %, divmod(), pow(), **, <<, >>, &, ^, |). For
instance, to evaluate the expression x + y, where x is an instance of
a class that has an __add__() method, x.__add__(y) is called. The
__divmod__() method should be the equivalent to using __floordiv__()
and __mod__(); it should not be related to __truediv__() (described
below). Note that __pow__() should be defined to accept an optional
third argument if the ternary version of the built-in pow() function
is to be supported.object.__complex__(self)
"""

    def __add__(self, other):
        """Supported operations with result types:

- bm + bm = bm
- bm + num = num
- num + bm = num (see radd)
"""
        if isinstance(other, numbers.Number):
            # bm + num
            return other + self.value
        else:
            # bm + bm
            total_bytes = self._byte_value + other.bytes
            return (type(self))(bytes=total_bytes)

    def __sub__(self, other):
        """Subtraction: Supported operations with result types:

- bm - bm = bm
- bm - num = num
- num - bm = num (see rsub)
"""
        if isinstance(other, numbers.Number):
            # bm - num
            return self.value - other
        else:
            # bm - bm
            total_bytes = self._byte_value - other.bytes
            return (type(self))(bytes=total_bytes)

    def __mul__(self, other):
        """Multiplication: Supported operations with result types:

- bm1 * bm2 = bm1
- bm * num = bm
- num * bm = bm (see rmul)
"""
        if isinstance(other, numbers.Number):
            # bm * num
            result = self._byte_value * other
            return (type(self))(bytes=result)
        else:
            # bm1 * bm2
            _other = other.value * other.base ** other.power
            _self = self.prefix_value * self._base ** self._power
            return (type(self))(bytes=_other * _self)

    def __truediv__(self, other):
        """Division: Supported operations with result types:

- bm1 / bm2 = num
- bm / num = bm
- num / bm = num (see rtruediv)
"""
        if isinstance(other, numbers.Number):
            # bm / num
            result = self._byte_value / other
            return (type(self))(bytes=result)
        else:
            # bm1 / bm2
            return self._byte_value / float(other.bytes)

    def __floordiv__(self, other):
        """Floor division: Supported operations with result types:

- bm1 // bm2 = int (whole divisions, unitless — mirrors bm1 / bm2 returning a ratio)
- bm // num  = bm (LHS type)
"""
        if isinstance(other, numbers.Number):
            # bm // num
            result = self._byte_value // other
            return (type(self))(bytes=result)
        else:
            # bm1 // bm2
            return int(self._byte_value // other.bytes)

    def __mod__(self, other):
        """Modulo (remainder): Supported operations with result types:

- bm1 % bm2 = bm (LHS type) — remainder after floor-dividing bm1 by bm2
- bm % num  = bm (LHS type)
"""
        if isinstance(other, numbers.Number):
            # bm % num
            result = self._byte_value % other
            return (type(self))(bytes=result)
        else:
            # bm1 % bm2
            return (type(self))(bytes=self._byte_value % other.bytes)

    def __divmod__(self, other):
        """divmod(bm, other) == (bm // other, bm % other).

Result types match __floordiv__ and __mod__.
"""
        return (self.__floordiv__(other), self.__mod__(other))

    ##################################################################

    """These methods are called to implement the binary arithmetic
operations (+, -, *, /, %, divmod(), pow(), **, <<, >>, &, ^, |) with
reflected (swapped) operands. These functions are only called if the
left operand does not support the corresponding operation and the
operands are of different types. [2] For instance, to evaluate the
expression x - y, where y is an instance of a class that has an
__rsub__() method, y.__rsub__(x) is called if x.__sub__(y) returns
NotImplemented.

These are the add/sub/mul/div methods for syntax where a number type
is given for the LTYPE and a bitmath object is given for the
RTYPE. E.g., 3 * MiB(3), or 10 / GB(42)
"""

    def __radd__(self, other):
        # Special case: 0 + bm = bm (identity element, enables built-in sum())
        if other == 0:
            return self
        # num + bm = num
        return other + self.value

    def __rsub__(self, other):
        # num - bm = num
        return other - self.value

    def __rmul__(self, other):
        # num * bm = bm
        return self * other

    def __rtruediv__(self, other):
        # num / bm = num
        return other / float(self.value)

    """Called to implement the built-in functions complex(), int(), and
float(). Should return a value of the appropriate type.

If one of those methods does not support the operation with the
supplied arguments, it should return NotImplemented.

For bitmath purposes, these methods return the int/float
equivalent of the this instances prefix Unix value. That is to say:

    - int(KiB(3.336)) would return 3
    - float(KiB(3.336)) would return 3.336
"""

    def __int__(self) -> int:
        """Return this instances prefix unit as an integer"""
        return int(self.prefix_value)

    def __float__(self) -> float:
        """Return this instances prefix unit as a floating point number"""
        return float(self.prefix_value)

    """floor/ceil/round operate on the prefix value and return the same unit
type. They are explicit opt-in operations for when integer prefix values are
needed. See the Rules for Math appendix in the bitmath documentation for the
design rationale behind floating-point representation.
"""

    def __floor__(self):
        """Return the largest integer prefix value <= this instance as the same type.

Rounds the prefix value down. math.floor(MiB(1.9)) -> MiB(1).
"""
        return (type(self))(math.floor(self.prefix_value))

    def __ceil__(self):
        """Return the smallest integer prefix value >= this instance as the same type.

Rounds the prefix value up. math.ceil(MiB(1.1)) -> MiB(2).
"""
        return (type(self))(math.ceil(self.prefix_value))

    def __round__(self, ndigits=None):
        """Return this instance rounded to ndigits precision as the same type.

round(MiB(1.75)) -> MiB(2); round(KiB(1.555), 2) -> KiB(1.56).

Rounds the prefix value using Python's built-in round(). When ndigits
is omitted the result has an integer prefix value. Only round at the
final output step; rounding intermediate results loses precision.
"""
        if ndigits is None:
            return (type(self))(round(self.prefix_value))
        return (type(self))(round(self.prefix_value, ndigits))

    ##################################################################
    # Bitwise operations
    ##################################################################

    def __lshift__(self, other):
        """Left shift, ex: 100 << 2

A left shift by n bits is equivalent to multiplication by pow(2,
n). A long integer is returned if the result exceeds the range of
plain integers."""
        shifted = int(self.bits) << other
        return type(self)(bits=shifted)

    def __rshift__(self, other):
        """Right shift, ex: 100 >> 2

A right shift by n bits is equivalent to division by pow(2, n)."""
        shifted = int(self.bits) >> other
        return type(self)(bits=shifted)

    def __and__(self, other):
        """"Bitwise and, ex: 100 & 2

bitwise and". Each bit of the output is 1 if the corresponding bit
of x AND of y is 1, otherwise it's 0."""
        andd = int(self.bits) & other
        return type(self)(bits=andd)

    def __xor__(self, other):
        """Bitwise xor, ex: 100 ^ 2

Does a "bitwise exclusive or". Each bit of the output is the same
as the corresponding bit in x if that bit in y is 0, and it's the
complement of the bit in x if that bit in y is 1."""
        xord = int(self.bits) ^ other
        return type(self)(bits=xord)

    def __or__(self, other):
        """Bitwise or, ex: 100 | 2

Does a "bitwise or". Each bit of the output is 0 if the corresponding
bit of x AND of y is 0, otherwise it's 1."""
        ord = int(self.bits) | other
        return type(self)(bits=ord)

    ##################################################################

    def __neg__(self):
        """The negative version of this instance"""
        return (type(self))(-abs(self.prefix_value))

    def __pos__(self):
        return (type(self))(abs(self.prefix_value))

    def __abs__(self):
        return (type(self))(abs(self.prefix_value))

    # def __invert__(self):
    #     """Called to implement the unary arithmetic operations (-, +, abs()
    #     and ~)."""
    #     return NotImplemented


######################################################################
# First, the bytes...

class Byte(Bitmath):
    """Byte based types fundamentally operate on self._bit_value"""
    def _setup(self):
        return (2, 0, 'B', 'B')

######################################################################
# NIST Prefixes for Byte based types


class KiB(Byte):
    def _setup(self):
        return (2, 10, 'KiB', 'KiBs')


Kio = KiB


class MiB(Byte):
    def _setup(self):
        return (2, 20, 'MiB', 'MiBs')


Mio = MiB


class GiB(Byte):
    def _setup(self):
        return (2, 30, 'GiB', 'GiBs')


Gio = GiB


class TiB(Byte):
    def _setup(self):
        return (2, 40, 'TiB', 'TiBs')


Tio = TiB


class PiB(Byte):
    def _setup(self):
        return (2, 50, 'PiB', 'PiBs')


Pio = PiB


class EiB(Byte):
    def _setup(self):
        return (2, 60, 'EiB', 'EiBs')


Eio = EiB


class ZiB(Byte):
    def _setup(self):
        return (2, 70, 'ZiB', 'ZiBs')


Zio = ZiB


class YiB(Byte):
    def _setup(self):
        return (2, 80, 'YiB', 'YiBs')


Yio = YiB


######################################################################
# SI Prefixes for Byte based types
class kB(Byte):
    def _setup(self):
        return (10, 3, 'kB', 'kBs')


ko = kB


class MB(Byte):
    def _setup(self):
        return (10, 6, 'MB', 'MBs')


Mo = MB


class GB(Byte):
    def _setup(self):
        return (10, 9, 'GB', 'GBs')


Go = GB


class TB(Byte):
    def _setup(self):
        return (10, 12, 'TB', 'TBs')


To = TB


class PB(Byte):
    def _setup(self):
        return (10, 15, 'PB', 'PBs')


Po = PB


class EB(Byte):
    def _setup(self):
        return (10, 18, 'EB', 'EBs')


Eo = EB


class ZB(Byte):
    def _setup(self):
        return (10, 21, 'ZB', 'ZBs')


Zo = ZB


class YB(Byte):
    def _setup(self):
        return (10, 24, 'YB', 'YBs')


Yo = YB


######################################################################
# And now the bit types
class Bit(Bitmath):
    """Bit based types fundamentally operate on self._bit_value"""

    def _set_prefix_value(self):
        self.prefix_value = self._to_prefix_value(self._bit_value)

    def _setup(self):
        return (2, 0, 'b', 'b')

    def _norm(self, value):
        """Normalize the input value into the fundamental unit for this prefix
type"""
        self._bit_value = value * self._unit_value
        self._byte_value = self._bit_value / 8.0


######################################################################
# NIST Prefixes for Bit based types
class Kib(Bit):
    def _setup(self):
        return (2, 10, 'Kib', 'Kibs')


class Mib(Bit):
    def _setup(self):
        return (2, 20, 'Mib', 'Mibs')


class Gib(Bit):
    def _setup(self):
        return (2, 30, 'Gib', 'Gibs')


class Tib(Bit):
    def _setup(self):
        return (2, 40, 'Tib', 'Tibs')


class Pib(Bit):
    def _setup(self):
        return (2, 50, 'Pib', 'Pibs')


class Eib(Bit):
    def _setup(self):
        return (2, 60, 'Eib', 'Eibs')


class Zib(Bit):
    def _setup(self):
        return (2, 70, 'Zib', 'Zibs')


class Yib(Bit):
    def _setup(self):
        return (2, 80, 'Yib', 'Yibs')


######################################################################
# SI Prefixes for Bit based types
class kb(Bit):
    def _setup(self):
        return (10, 3, 'kb', 'kbs')


class Mb(Bit):
    def _setup(self):
        return (10, 6, 'Mb', 'Mbs')


class Gb(Bit):
    def _setup(self):
        return (10, 9, 'Gb', 'Gbs')


class Tb(Bit):
    def _setup(self):
        return (10, 12, 'Tb', 'Tbs')


class Pb(Bit):
    def _setup(self):
        return (10, 15, 'Pb', 'Pbs')


class Eb(Bit):
    def _setup(self):
        return (10, 18, 'Eb', 'Ebs')


class Zb(Bit):
    def _setup(self):
        return (10, 21, 'Zb', 'Zbs')


class Yb(Bit):
    def _setup(self):
        return (10, 24, 'Yb', 'Ybs')


######################################################################
# Utility functions
def best_prefix(bytes: Bitmath | int | float, system: int = NIST) -> Bitmath:
    """Return a bitmath instance representing the best human-readable
representation of the number of bytes given by ``bytes``. In addition
to a numeric type, the ``bytes`` parameter may also be a bitmath type.

Optionally select a preferred unit system by specifying the ``system``
keyword. Choices for ``system`` are ``bitmath.NIST`` (default) and
``bitmath.SI``.

Basically a shortcut for:

   >>> import bitmath
   >>> b = bitmath.Byte(12345)
   >>> best = b.best_prefix()

Or:

   >>> import bitmath
   >>> best = (bitmath.KiB(12345) * 4201).best_prefix()
    """
    if isinstance(bytes, Bitmath):
        value = bytes.bytes
    else:
        value = bytes
    return Byte(value).best_prefix(system=system)


def _query_device_capacity_windows(device_fd: IO[Any]) -> int:
    """Return device capacity in bytes on Windows via DeviceIoControl.

Windows physical disk paths look like ``\\\\.\\PhysicalDrive0``.
Raises :class:`ValueError` if the file descriptor is not a physical device.
Raises :class:`OSError` if the DeviceIoControl call fails.
"""
    if not device_fd.name.startswith('\\\\.\\'):
        raise ValueError("The file descriptor provided is not of a device type")

    IOCTL_DISK_GET_DRIVE_GEOMETRY_EX = 0x000700A0

    class DISK_GEOMETRY(ctypes.Structure):
        _fields_ = [
            ('Cylinders', ctypes.c_longlong),
            ('MediaType', ctypes.c_uint),
            ('TracksPerCylinder', ctypes.c_ulong),
            ('SectorsPerTrack', ctypes.c_ulong),
            ('BytesPerSector', ctypes.c_ulong),
        ]

    class DISK_GEOMETRY_EX(ctypes.Structure):
        _fields_ = [
            ('Geometry', DISK_GEOMETRY),
            ('DiskSize', ctypes.c_longlong),
            ('Data', ctypes.c_byte * 1),
        ]

    geometry = DISK_GEOMETRY_EX()
    bytes_returned = ctypes.wintypes.DWORD(0)
    handle = msvcrt.get_osfhandle(device_fd.fileno())

    result = ctypes.windll.kernel32.DeviceIoControl(
        handle,
        IOCTL_DISK_GET_DRIVE_GEOMETRY_EX,
        None,
        0,
        ctypes.byref(geometry),
        ctypes.sizeof(geometry),
        ctypes.byref(bytes_returned),
        None,
    )

    if not result:
        error_code = ctypes.windll.kernel32.GetLastError()
        raise OSError(f"DeviceIoControl failed with error code: {error_code}")

    return geometry.DiskSize


def query_device_capacity(device_fd: IO[Any]) -> Byte:
    """Create bitmath instances of the capacity of a system block device

Make one or more ioctl request to query the capacity of a block
device. Perform any processing required to compute the final capacity
value. Return the device capacity in bytes as a :class:`bitmath.Byte`
instance.

Thanks to the following resources for help figuring this out Linux/Mac
ioctl's for querying block device sizes:

* http://stackoverflow.com/a/12925285/263969
* http://stackoverflow.com/a/9764508/263969

   :param file device_fd: A ``file`` object of the device to query the
   capacity of. On Linux/macOS: ``open("/dev/sda", "rb")``. On Windows:
   ``open(r'\\\\.\\PhysicalDrive0', 'rb')`` (requires administrator privileges).

   :return: a bitmath :class:`bitmath.Byte` instance equivalent to the
   capacity of the target device in bytes.
"""
    if os.name not in SUPPORTED_PLATFORMS:
        raise NotImplementedError(f"'bitmath.query_device_capacity' is not supported on this platform: {os.name}")
    if os.name == 'nt':
        return Byte(_query_device_capacity_windows(device_fd))

    s = os.stat(device_fd.name).st_mode
    if not stat.S_ISBLK(s):
        raise ValueError("The file descriptor provided is not of a device type")

    # The keys of the ``ioctl_map`` dictionary correlate to possible
    # values from the ``platform.system`` function.
    ioctl_map = {
        # ioctls for the "Linux" platform
        "Linux": {
            "request_params": [
                # A list of parameters to calculate the block size.
                #
                # ( PARAM_NAME , FORMAT_CHAR , REQUEST_CODE )
                ("BLKGETSIZE64", "L", 0x80081272)
                # Per <linux/fs.h>, the BLKGETSIZE64 request returns a
                # 'u64' sized value. This is an unsigned 64 bit
                # integer C type. This means to correctly "buffer" the
                # result we need 64 bits, or 8 bytes, of memory.
                #
                # The struct module documentation include a reference
                # chart relating formatting characters to native C
                # Types. In this case, using the "native size", the
                # table tells us:
                #
                # * Character 'L' - Unsigned Long C Type (u64) - Loads into a Python int type
                #
                # Confirm this character is right by running (on Linux):
                #
                #    >>> import struct
                #    >>> print(8 == struct.calcsize('L'))
                #
                # The result should be true as long as your kernel
                # headers define BLKGETSIZE64 as a u64 type (please
                # file a bug report at
                # https://github.com/timlnx/bitmath/issues/new if
                # this does *not* work for you)
            ],
            # func is how the final result is decided. Because the
            # Linux BLKGETSIZE64 call returns the block device
            # capacity in bytes as an integer value, no extra
            # calculations are required. Simply return the value of
            # BLKGETSIZE64.
            "func": lambda x: x["BLKGETSIZE64"]
        },
        # ioctls for the "Darwin" (Mac OS X) platform
        "Darwin": {
            "request_params": [
                # A list of parameters to calculate the block size.
                #
                # ( PARAM_NAME , FORMAT_CHAR , REQUEST_CODE )
                ("DKIOCGETBLOCKCOUNT", "L", 0x40086419),
                # Per <sys/disk.h>: get media's block count - uint64_t
                #
                # As in the BLKGETSIZE64 example, an unsigned 64 bit
                # integer will use the 'L' formatting character
                ("DKIOCGETBLOCKSIZE", "I", 0x40046418)
                # Per <sys/disk.h>: get media's block size - uint32_t
                #
                # This request returns an unsigned 32 bit integer, or
                # in other words: just a normal integer (or 'int' c
                # type). That should require 4 bytes of space for
                # buffering. According to the struct modules
                # 'Formatting Characters' chart:
                #
                # * Character 'I' - Unsigned Int C Type (uint32_t) - Loads into a Python int type
            ],
            # OS X doesn't have a direct equivalent to the Linux
            # BLKGETSIZE64 request. Instead, we must request how many
            # blocks (or "sectors") are on the disk, and the size (in
            # bytes) of each block. Finally, multiply the two together
            # to obtain capacity:
            #
            #                      n Block * y Byte
            # capacity (bytes)  =            -------
            #                                1 Block
            "func": lambda x: x["DKIOCGETBLOCKCOUNT"] * x["DKIOCGETBLOCKSIZE"]
            # This expression simply accepts a dictionary ``x`` as a
            # parameter, and then returns the result of multiplying
            # the two named dictionary items together. In this case,
            # that means multiplying ``DKIOCGETBLOCKCOUNT``, the total
            # number of blocks, by ``DKIOCGETBLOCKSIZE``, the size of
            # each block in bytes.
        }
    }

    platform_params = ioctl_map[platform.system()]
    results = {}

    for req_name, fmt, request_code in platform_params['request_params']:
        # Read the systems native size (in bytes) of this format type.
        buffer_size = struct.calcsize(fmt)
        # This code has been ran on only a few test systems. If it's
        # appropriate, maybe in the future we'll add try/except
        # conditions for some possible errors. Really only for cases
        # where it would add value to override the default exception
        # message string.
        buffer = fcntl.ioctl(device_fd.fileno(), request_code, buffer_size)

        # Unpack the raw result from the ioctl call into a familiar
        # python data type according to the ``fmt`` rules.
        result = struct.unpack(fmt, buffer)[0]
        # Add the new result to our collection
        results[req_name] = result

    return Byte(platform_params['func'](results))


def getsize(path: str, bestprefix: bool = True, system: int = NIST) -> Bitmath:
    """Return a bitmath instance in the best human-readable representation
of the file size at `path`. Optionally, provide a preferred unit
system by setting `system` to either `bitmath.NIST` (default) or
`bitmath.SI`.

Optionally, set ``bestprefix`` to ``False`` to get ``bitmath.Byte``
instances back.
    """
    _path = os.path.realpath(path)
    size_bytes = os.path.getsize(_path)
    if bestprefix:
        return Byte(size_bytes).best_prefix(system=system)
    else:
        return Byte(size_bytes)


def listdir(
    search_base: str,
    followlinks: bool = False,
    filter: str = '*',
    relpath: bool = False,
    bestprefix: bool = False,
    system: int = NIST,
) -> Iterator[tuple[str, Bitmath]]:
    """This is a generator which recurses the directory tree
`search_base`, yielding 2-tuples of:

* The absolute/relative path to a discovered file
* A bitmath instance representing the "apparent size" of the file.

    - `search_base` - The directory to begin walking down.
    - `followlinks` - Whether or not to follow symbolic links to directories
    - `filter` - A glob (see :py:mod:`fnmatch`) to filter results with
      (default: ``*``, everything)
    - `relpath` - ``True`` to return the relative path from `pwd` or
      ``False`` (default) to return the fully qualified path
    - ``bestprefix`` - set to ``False`` to get ``bitmath.Byte``
      instances back instead.
    - `system` - Provide a preferred unit system by setting `system`
      to either ``bitmath.NIST`` (default) or ``bitmath.SI``.

.. note:: This function does NOT return tuples for directory entities.

.. note:: Symlinks to **files** are followed automatically

    """
    for root, dirs, files in os.walk(search_base, followlinks=followlinks):
        for name in fnmatch.filter(files, filter):
            _path = os.path.join(root, name)
            if relpath:
                # RELATIVE path
                _return_path = os.path.relpath(_path, '.')
            else:
                # REAL path
                _return_path = os.path.realpath(_path)

            if followlinks:
                yield (_return_path, getsize(_path, bestprefix=bestprefix, system=system))
            else:
                if os.path.isdir(_path) or os.path.islink(_path):
                    pass  # pragma: no cover
                else:
                    yield (_return_path, getsize(_path, bestprefix=bestprefix, system=system))


def parse_string(s: str | numbers.Number, system: int = NIST, strict: bool = True) -> Bitmath:
    """Parse a string with units and return a bitmath instance.

String inputs may include whitespace characters between the value and
the unit.

:param s: The string to parse.
:param system: Unit system to use when ``strict=False``. Ignored when
    ``strict=True`` (the default). Set to ``bitmath.NIST`` (default)
    or ``bitmath.SI``.
:param strict: When ``True`` (default), the unit must be an exact
    bitmath type name (e.g. ``"KiB"``, ``"MB"``). When ``False``,
    accepts ambiguous input such as plain numbers, numeric strings,
    and case-insensitive single-letter units (e.g. ``"4k"``,
    ``"2.7M"``); see caveats below.

When ``strict=False`` the following rules apply:

* All inputs are assumed to be byte-based (not bit-based)
* Plain numbers and numeric strings are assumed to be bytes
* Single-letter units (``k``, ``M``, ``G``, etc.) are assumed NIST
  unless ``system=bitmath.SI``
* Inputs with an ``i`` after the leading letter (``Ki``, ``Mi``)
  are treated as NIST units
* Capitalisation does not matter

The result is returned in the parsed unit system. To coerce the result
into a preferred unit system call ``.best_prefix(system=system)`` on
the return value::

    parse_string("4k", strict=False).best_prefix(system=bitmath.SI)

.. versionchanged:: 2.0.0
   Added ``strict`` and ``system`` parameters. When ``strict=True``
   (default) behavior is identical to the original function.
   When ``strict=False`` the behavior of the former
   ``parse_string_unsafe`` is applied. The ``system`` parameter
   defaults to ``bitmath.NIST`` and is ignored when ``strict=True``.
    """
    if strict:
        # Strings only please
        if not isinstance(s, str):
            raise ValueError(f"parse_string only accepts string inputs but a {type(s)} was given")

        # get the index of the first alphabetic character
        try:
            index = next(i for i, c in enumerate(s) if c.isalpha())
        except StopIteration:
            # If there's no alphabetic characters we won't be able to find a match
            raise ValueError(f"No unit detected, can not parse string '{s}' into a bitmath object")

        # split the string into the value and the unit
        val, unit = s[:index], s[index:]

        # see if the unit exists as a type in our namespace
        if unit == "b":
            unit_class = Bit
        elif unit == "B":
            unit_class = Byte
        else:
            if not (hasattr(sys.modules[__name__], unit) and isinstance(getattr(sys.modules[__name__], unit), type)):
                raise ValueError(f"The unit {unit} is not a valid bitmath unit")
            unit_class = globals()[unit]

        try:
            val = float(val)
        except ValueError:
            raise
        try:
            return unit_class(val)
        except:  # pragma: no cover
            raise ValueError(f"Can't parse string {s} into a bitmath object")

    else:
        # strict=False path (formerly parse_string_unsafe)
        if not isinstance(s, str) and not isinstance(s, numbers.Number):
            raise ValueError(f"parse_string only accepts string/number inputs but a {type(s)} was given")

        # Test case: raw number input (easy!)
        if isinstance(s, numbers.Number):
            return Byte(s)

        # Test case: a number pretending to be a string
        if isinstance(s, str):
            try:
                return Byte(float(s))
            except ValueError:
                pass

        # At this point the input is a string with a unit component.
        # Separate the number and the unit.
        try:
            index = next(i for i, c in enumerate(s) if c.isalpha())
        except StopIteration:  # pragma: no cover
            raise ValueError(f"No unit detected, can not parse string '{s}' into a bitmath object")

        val, unit = s[:index], s[index:]

        # Explicit base-unit and word-form checks: handle B, b, bit(s),
        # byte(s) before the prefix-normalization logic below.
        _unit_lower = unit.lower()
        if unit == 'B' or _unit_lower in ('byte', 'bytes'):
            return Byte(float(val))
        if unit == 'b' or _unit_lower in ('bit', 'bits'):
            return Bit(float(val))

        # Normalise: strip trailing b/B and append 'B' so we always
        # work with byte-family units regardless of what was supplied.
        unit = unit.rstrip('Bb')
        unit += 'B'

        if len(unit) == 2:
            if system == NIST:
                unit = capitalize_first(unit)
                _unit = list(unit)
                _unit.insert(1, 'i')
                unit = ''.join(_unit)
                if unit in globals():
                    unit_class = globals()[unit]
            else:
                if unit.startswith('K'):
                    unit = unit.replace('K', 'k')
                elif not unit.startswith('k'):
                    unit = capitalize_first(unit)
                if unit[0] in SI_PREFIXES:
                    unit_class = globals()[unit]
        elif len(unit) == 3:
            unit = capitalize_first(unit)
            if unit[:2] in NIST_PREFIXES:
                unit_class = globals()[unit]
        else:
            raise ValueError(f"The unit {unit} is not a valid bitmath unit")

        try:
            unit_class
        except UnboundLocalError:
            raise ValueError(f"The unit {unit} is not a valid bitmath unit")

        return unit_class(float(val))


def parse_string_unsafe(s: str | numbers.Number, system: int = NIST) -> Bitmath:
    """Deprecated wrapper for ``parse_string(s, strict=False, system=system)``.

.. deprecated:: 2.0.0
   ``parse_string_unsafe`` is deprecated and will be removed in a
   future release. Use ``parse_string(s, strict=False,
   system=system)`` instead.

   To suppress this warning::

       import warnings
       warnings.filterwarnings('ignore', category=DeprecationWarning,
                               module='bitmath')
    """
    import warnings
    warnings.warn(
        "parse_string_unsafe is deprecated as of 2.0.0 and will be removed "
        "in a future release. Use parse_string(s, strict=False, system=system) "
        "instead. To suppress: "
        "warnings.filterwarnings('ignore', category=DeprecationWarning, module='bitmath')",
        DeprecationWarning,
        stacklevel=2,
    )
    return parse_string(s, system=system, strict=False)


def sum(iterable: Iterable[Bitmath], start: Bitmath | None = None) -> Bitmath:
    """Sum an iterable of bitmath instances, returning a Byte by default.

The built-in sum() also works with bitmath objects: the __radd__
identity (0 + bm = bm) means sum() preserves the type of the first
element. Use bitmath.sum() instead when you need the result normalised
to a specific unit regardless of input types — it accumulates into
Byte(0) by default, or into the provided start instance.

- bitmath.sum([MiB(1), GiB(1)]) -> Byte(1074790400.0)
- bitmath.sum([KiB(1), KiB(2)], start=MiB(0)) -> MiB(0.0029296875)
"""
    result = Byte(0) if start is None else start
    for item in iterable:
        result = result + item
    return result


######################################################################
# Context Managers
@contextlib.contextmanager
def format(fmt_str: str | None = None, plural: bool = False, bestprefix: bool = False) -> Generator[None, None, None]:
    """Thread-safe context manager for printing bitmath instances.

``fmt_str`` - a formatting mini-language compatible string. See
the @properties (above) for a list of available items.

``plural`` - True enables printing instances with 's' if they're
plural. False (default) prints them as singular (no trailing 's').

``bestprefix`` - True converts instances to their best human-readable
prefix unit before formatting. False (default) formats the instance
as its current prefix unit.

All settings are thread-local: concurrent contexts in different threads
are fully isolated from one another. Nested contexts within the same
thread correctly save and restore the enclosing context's settings.
    """
    prev_fmt = getattr(_thread_local, 'format_string', _FMT_SENTINEL)
    prev_plural = getattr(_thread_local, 'format_plural', _FMT_SENTINEL)
    prev_bestprefix = getattr(_thread_local, 'bestprefix', _FMT_SENTINEL)

    _thread_local.format_string = fmt_str if fmt_str is not None else format_string
    _thread_local.format_plural = plural
    _thread_local.bestprefix = bestprefix

    try:
        yield
    finally:
        if prev_fmt is _FMT_SENTINEL:
            del _thread_local.format_string
        else:
            _thread_local.format_string = prev_fmt
        if prev_plural is _FMT_SENTINEL:
            del _thread_local.format_plural
        else:
            _thread_local.format_plural = prev_plural
        if prev_bestprefix is _FMT_SENTINEL:
            del _thread_local.bestprefix
        else:
            _thread_local.bestprefix = prev_bestprefix


def cli_script_main(cli_args):
    """
    A command line interface to basic bitmath operations.
    """
    choices = ALL_UNIT_TYPES

    parser = argparse.ArgumentParser(
        description='Converts from one type of size to another.')
    parser.add_argument('--from-stdin', default=False, action='store_true',
                        help='Reads number from stdin rather than the cli')
    parser.add_argument(
        '-f', '--from', choices=choices, nargs=1,
        type=str, dest='fromunit', default=['Byte'],
        help='Input type you are converting from. Defaultes to Byte.')
    parser.add_argument(
        '-t', '--to', choices=choices, required=False, nargs=1, type=str,
        help=('Input type you are converting to. '
              'Attempts to detect best result if omitted.'), dest='tounit')
    parser.add_argument(
        'size', nargs='*', type=float,
        help='The number to convert.')

    args = parser.parse_args(cli_args)

    # Not sure how to cover this with tests, or if the functionality
    # will remain in this form long enough for it to make writing a
    # test worth the effort.
    if args.from_stdin:  # pragma: no cover
        args.size = [float(sys.stdin.readline()[:-1])]

    results = []

    for size in args.size:
        instance = getattr(__import__(
            'bitmath', fromlist=['True']), args.fromunit[0])(size)

        # If we have a unit provided then use it
        if args.tounit:
            result = getattr(instance, args.tounit[0])
        # Otherwise use the best_prefix call
        else:
            result = instance.best_prefix()

        results.append(result)

    return results


def cli_script():  # pragma: no cover
    # Wrapper around cli_script_main so we can unittest the command
    # line functionality
    for result in cli_script_main(sys.argv[1:]):
        print(result)


if __name__ == '__main__':
    cli_script()
