.. image:: https://api.travis-ci.org/tbielawa/bitmath.png
   :target: https://travis-ci.org/tbielawa/bitmath/
   :align: right
   :height: 19
   :width: 77

.. image:: https://coveralls.io/repos/tbielawa/bitmath/badge.png?branch=master
   :target: https://coveralls.io/github/tbielawa/bitmath
   :align: right
   :height: 19
   :width: 77


bitmath
#######

`bitmath <http://bitmath.readthedocs.org/en/latest/>`_ simplifies many
facets of interacting with file sizes in various units. Originally
focusing on file size unit conversion, functionality now includes:

* Converting between **SI** and **NIST** prefix units (``kB`` to ``GiB``)
* Converting between units of the same type (SI to SI, or NIST to NIST)
* Automatic human-readable prefix selection (like in `hurry.filesize <https://pypi.python.org/pypi/hurry.filesize>`_)
* Basic arithmetic operations (subtracting 42KiB from 50GiB)
* Rich comparison operations (``1024 Bytes == 1KiB``)
* bitwise operations (``<<``, ``>>``, ``&``, ``|``, ``^``)
* Reading a device's storage capacity (Linux/OS X support only)
* String parsing
* Sorting
* `argparse <https://docs.python.org/3/library/argparse.html>`_
  integration as a custom type

In addition to the conversion and math operations, `bitmath` provides
human readable representations of values which are suitable for use in
interactive shells as well as larger scripts and applications. The
format produced for these representations is customizable via the
functionality included in stdlibs `string.format
<https://docs.python.org/3/library/string.html>`_.

In discussion we will refer to the NIST units primarily. I.e., instead
of "megabyte" we will refer to "mebibyte". The former is ``10^3 =
1,000,000`` bytes, whereas the second is ``2^20 = 1,048,576``
bytes. When you see file sizes or transfer rates in your web browser,
most of the time what you're really seeing are the base-2 sizes/rates.

**Don't Forget!** The source for bitmath `is available on GitHub
<https://github.com/tbielawa/bitmath>`_.

And did we mention there's almost 200 unittests? `Check them out for
yourself <https://github.com/tbielawa/bitmath/tree/master/tests>`_.

* :ref:`Examples <index_examples>` after the TOC.


Installation
############

The easiest way to install bitmath is via ``dnf`` (or ``yum``) if
you're on a Fedora/RHEL based distribution. bitmath is available in
the main Fedora repositories, as well as EPEL Repositories. As of 2023
bitmath is only developed, tested, and supported for `currently
supported <https://devguide.python.org/versions/>`_ Python releases.


.. code-block:: bash

   $ sudo dnf install python3-bitmath


**PyPi**:

You could also install bitmath from `PyPi
<https://pypi.python.org/pypi/bitmath>`_ if you like:

.. code-block:: bash

   $ sudo pip install bitmath

.. note::

   **pip** installs need pip >= 1.1. To workaround this, `download
   bitmath <https://pypi.python.org/pypi/bitmath/#downloads>`_, from
   PyPi and then ``pip install bitmath-x.y.z.tar.gz``. See `issue #57
   <https://github.com/tbielawa/bitmath/issues/57#issuecomment-227018168>`_
   for more information.



**Source**:

Or, if you want to install from source:

.. code-block:: bash

   $ sudo python ./setup.py install

If you want the bitmath manpage installed as well:

.. code-block:: bash

   $ sudo make install


Contents
########

.. toctree::
   :maxdepth: 2
   :numbered:

   module.rst
   commandline.rst
   classes.rst
   instances.rst
   simple_examples.rst
   real_life_examples.rst
   contributing.rst
   appendices.rst
   NEWS.rst
   contact.rst
   copyright.rst



.. _index_examples:

Examples
========


Arithmetic
----------

.. code-block:: python

   >>> import bitmath
   >>> log_size = bitmath.kB(137.4)
   >>> log_zipped_size = bitmath.Byte(987)
   >>> print "Compression saved %s space" % (log_size - log_zipped_size)
   Compression saved 136.413kB space
   >>> thumb_drive = bitmath.GiB(12)
   >>> song_size = bitmath.MiB(5)
   >>> songs_per_drive = thumb_drive / song_size
   >>> print songs_per_drive
   2457.6


Convert Units
-------------

File size unit conversion:

.. code-block:: python

   >>> from bitmath import *
   >>> dvd_size = GiB(4.7)
   >>> print "DVD Size in MiB: %s" % dvd_size.to_MiB()
   DVD Size in MiB: 4812.8 MiB


Select a human-readable unit
----------------------------

.. code-block:: python

   >>> small_number = kB(100)
   >>> ugly_number = small_number.to_TiB()

   >>> print ugly_number
   9.09494701773e-08 TiB
   >>> print ugly_number.best_prefix()
   97.65625 KiB


Rich Comparison
---------------

.. code-block:: python

   >>> cd_size = MiB(700)
   >>> cd_size > dvd_size
   False
   >>> cd_size < dvd_size
   True
   >>> MiB(1) == KiB(1024)
   True
   >>> MiB(1) <= KiB(1024)
   True

Sorting
-------

.. code-block:: python

   >>> sizes = [KiB(7337.0), KiB(1441.0), KiB(2126.0), KiB(2178.0),
                     KiB(2326.0), KiB(4003.0), KiB(48.0), KiB(1770.0),
                     KiB(7892.0), KiB(4190.0)]

   >>> print sorted(sizes)
   [KiB(48.0), KiB(1441.0), KiB(1770.0), KiB(2126.0), KiB(2178.0),
   KiB(2326.0), KiB(4003.0), KiB(4190.0), KiB(7337.0), KiB(7892.0)]


Custom Formatting
-----------------

* Use of the custom formatting system
* All of the available instance properties

Example:

.. code-block:: python

   >>> longer_format = """Formatting attributes for %s
      ...: This instances prefix unit is {unit}, which is a {system} type unit
      ...: The unit value is {value}
      ...: This value can be truncated to just 1 digit of precision: {value:.1f}
      ...: In binary this looks like: {binary}
      ...: The prefix unit is derived from a base of {base}
      ...: Which is raised to the power {power}
      ...: There are {bytes} bytes in this instance
      ...: The instance is {bits} bits large
      ...: bytes/bits without trailing decimals: {bytes:.0f}/{bits:.0f}""" % str(ugly_number)

   >>> print ugly_number.format(longer_format)
   Formatting attributes for 5.96046447754 MiB
   This instances prefix unit is MiB, which is a NIST type unit
   The unit value is 5.96046447754
   This value can be truncated to just 1 digit of precision: 6.0
   In binary this looks like: 0b10111110101111000010000000
   The prefix unit is derived from a base of 2
   Which is raised to the power 20
   There are 6250000.0 bytes in this instance
   The instance is 50000000.0 bits large
   bytes/bits without trailing decimals: 6250000/50000000

Utility Functions
-----------------

**bitmath.getsize()**

.. code-block:: python

   >>> print bitmath.getsize('python-bitmath.spec')
   3.7060546875 KiB

**bitmath.parse_string()**

Parse a string with standard units:

.. code-block:: python

   >>> import bitmath
   >>> a_dvd = bitmath.parse_string("4.7 GiB")
   >>> print type(a_dvd)
   <class 'bitmath.GiB'>
   >>> print a_dvd
   4.7 GiB

**bitmath.parse_string_unsafe()**

Parse a string with ambiguous units:

.. code-block:: python

   >>> import bitmath
   >>> a_gig = bitmath.parse_string_unsafe("1gb")
   >>> print type(a_gig)
   <class 'bitmath.GB'>
   >>> a_gig == bitmath.GB(1)
   True
   >>> bitmath.parse_string_unsafe('1gb') == bitmath.parse_string_unsafe('1g')
   True


**bitmath.query_device_capacity()**

.. code-block:: python

   >>> import bitmath
   >>> with open('/dev/sda') as fp:
   ...     root_disk = bitmath.query_device_capacity(fp)
   ...     print root_disk.best_prefix()
   ...
   238.474937439 GiB

**bitmath.listdir()**

.. code-block:: python

   >>> for i in bitmath.listdir('./tests/', followlinks=True, relpath=True, bestprefix=True):
   ...     print i
   ...
   ('tests/test_file_size.py', KiB(9.2900390625))
   ('tests/test_basic_math.py', KiB(7.1767578125))
   ('tests/__init__.py', KiB(1.974609375))
   ('tests/test_bitwise_operations.py', KiB(2.6376953125))
   ('tests/test_context_manager.py', KiB(3.7744140625))
   ('tests/test_representation.py', KiB(5.2568359375))
   ('tests/test_properties.py', KiB(2.03125))
   ('tests/test_instantiating.py', KiB(3.4580078125))
   ('tests/test_future_math.py', KiB(2.2001953125))
   ('tests/test_best_prefix_BASE.py', KiB(2.1044921875))
   ('tests/test_rich_comparison.py', KiB(3.9423828125))
   ('tests/test_best_prefix_NIST.py', KiB(5.431640625))
   ('tests/test_unique_testcase_names.sh', Byte(311.0))
   ('tests/.coverage', KiB(3.1708984375))
   ('tests/test_best_prefix_SI.py', KiB(5.34375))
   ('tests/test_to_built_in_conversion.py', KiB(1.798828125))
   ('tests/test_to_Type_conversion.py', KiB(8.0185546875))
   ('tests/test_sorting.py', KiB(4.2197265625))
   ('tests/listdir_symlinks/10_byte_file_link', Byte(10.0))
   ('tests/listdir_symlinks/depth1/depth2/10_byte_file', Byte(10.0))
   ('tests/listdir_nosymlinks/depth1/depth2/10_byte_file', Byte(10.0))
   ('tests/listdir_nosymlinks/depth1/depth2/1024_byte_file', KiB(1.0))
   ('tests/file_sizes/kbytes.test', KiB(1.0))
   ('tests/file_sizes/bytes.test', Byte(38.0))
   ('tests/listdir/10_byte_file', Byte(10.0))


Formatting
----------

.. code-block:: python

   >>> with bitmath.format(fmt_str="[{value:.3f}@{unit}]"):
   ...     for i in bitmath.listdir('./tests/', followlinks=True, relpath=True, bestprefix=True):
   ...         print i[1]
   ...
   [9.290@KiB]
   [7.177@KiB]
   [1.975@KiB]
   [2.638@KiB]
   [3.774@KiB]
   [5.257@KiB]
   [2.031@KiB]
   [3.458@KiB]
   [2.200@KiB]
   [2.104@KiB]
   [3.942@KiB]
   [5.432@KiB]
   [311.000@Byte]
   [3.171@KiB]
   [5.344@KiB]
   [1.799@KiB]
   [8.019@KiB]
   [4.220@KiB]
   [10.000@Byte]
   [10.000@Byte]
   [10.000@Byte]
   [1.000@KiB]
   [1.000@KiB]
   [38.000@Byte]
   [10.000@Byte]

``argparse`` Integration
------------------------

Example script using ``bitmath.integrations.bmargparse.BitmathType`` as an
argparser argument type:

.. code-block:: python

   import argparse
   from bitmath.integrations.bmargparse import BitmathType
   parser = argparse.ArgumentParser(
       description="Arg parser with a bitmath type argument")
   parser.add_argument('--block-size',
                       type=BitmathType,
                       required=True)

   results = parser.parse_args()
   print "Parsed in: {PARSED}; Which looks like {TOKIB} as a Kibibit".format(
       PARSED=results.block_size,
       TOKIB=results.block_size.Kib)

If ran as a script the results would be similar to this:

.. code-block:: bash

   $ python ./bmargparse.py --block-size 100MiB
   Parsed in: 100.0 MiB; Which looks like 819200.0 Kib as a Kibibit
