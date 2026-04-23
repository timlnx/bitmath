.. _module:

.. py:module:: bitmath


The ``bitmath`` Module
######################

.. contents::
   :depth: 3
   :local:

Functions
*********

This section describes utility functions included in the
:py:mod:`bitmath` module.

.. _bitmath_getsize:

bitmath.getsize()
=================

.. function:: getsize(path[, bestprefix=True[, system=NIST]])

   Return a bitmath instance representing the size of a file at any
   given path.

   :param string path: The path of a file to read the size of
   :param bool bestprefix: **Default:** ``True``, the returned
                           instance will be in the best human-readable
                           prefix unit. If set to ``False`` the result
                           is a :class:`.Byte` instance.
   :param system: **Default:** :py:data:`bitmath.NIST`. The preferred
                  system of units for the returned instance.
   :type system: One of :py:data:`bitmath.NIST` or :py:data:`bitmath.SI`

   Internally :py:func:`bitmath.getsize` calls
   :py:func:`os.path.realpath` before calling
   :py:func:`os.path.getsize` on any paths.

   Here's an example of where we'll run :py:func:`bitmath.getsize` on
   the bitmath source code using the defaults for the ``bestprefix``
   and ``system`` parameters:

   .. code-block:: python

      >>> import bitmath
      >>> print(bitmath.getsize('./bitmath/__init__.py'))
      33.3583984375 KiB

   Let's say we want to see the results in bytes. We can do this by
   setting ``bestprefix`` to ``False``:

   .. code-block:: python

      >>> import bitmath
      >>> print(bitmath.getsize('./bitmath/__init__.py', bestprefix=False))
      34159.0 B

   Recall, the default for representation is with the best
   human-readable prefix. We can control the prefix system used by
   setting ``system`` to either :py:data:`bitmath.NIST` (the default)
   or :py:data:`bitmath.SI`:

   .. code-block:: python
      :linenos:
      :emphasize-lines: 1-4

      >>> print(bitmath.getsize('./bitmath/__init__.py'))
      33.3583984375 KiB
      >>> print(bitmath.getsize('./bitmath/__init__.py', system=bitmath.NIST))
      33.3583984375 KiB
      >>> print(bitmath.getsize('./bitmath/__init__.py', system=bitmath.SI))
      34.159 kB

   We can see in lines **1** → **4** that the same result is returned
   when ``system`` is not set and when ``system`` is set to
   :py:data:`bitmath.NIST` (the default).

   .. versionadded:: 1.0.7

bitmath.listdir()
=================

.. function:: listdir(search_base[, followlinks=False[, filter='*'[, relpath=False[, bestprefix=False[, system=NIST]]]]])

   This is a `generator
   <https://docs.python.org/3/tutorial/classes.html#generators>`_
   which recurses a directory tree yielding 2-tuples of:

   * The absolute/relative path to a discovered file
   * A bitmath instance representing the *apparent size* of the file

   :param string search_base: The directory to begin walking down
   :param bool followlinks: **Default:** ``False``, do not follow
                            links. Whether or not to follow symbolic
                            links to directories. Setting to ``True``
                            enables directory link following
   :param string filter: **Default:** ``*`` (everything). A glob to
                         filter results with. See `fnmatch
                         <https://docs.python.org/3/library/fnmatch.html>`_
                         for more details about *globs*
   :param bool relpath: **Default:** ``False``, returns the fully
                        qualified to each discovered file. ``True`` to
                        return the relative path from the present
                        working directory to the discovered file. If
                        ``relpath`` is ``False``, then
                        :py:func:`bitmath.listdir` internally calls
                        :py:func:`os.path.realpath` to normalize path
                        references
   :param bool bestprefix: **Default:** ``False``, returns
                           :class:`.Byte` instances. Set to ``True``
                           to return the best human-readable prefix
                           unit for representation
   :param system: **Default:** :py:data:`bitmath.NIST`. Set a prefix
                  preferred unit system. Requires ``bestprefix`` is
                  ``True``
   :type system: One of :py:data:`bitmath.NIST` or :py:data:`bitmath.SI`

   .. note::

      * This function does **not** return tuples for directory
        entities. Including directories in results is `scheduled for
        introduction <https://github.com/timlnx/bitmath/issues/27>`_
        in an upcoming release.
      * Symlinks to **files** are followed automatically


   When interpreting the results from this function it is *crucial* to
   understand exactly which items are being taken into account, what
   decisions were made to select those items, and how their sizes are
   measured.

   Results from this function may seem invalid when directly compared
   to the results from common command line utilities, such as ``du``,
   or ``tree``.

   Let's pretend we have a directory structure like the following::

      some_files/
      ├── deeper_files/
      │   └── second_file
      └── first_file

   Where ``some_files/`` is a directory, and so is
   ``some_files/deeper_files/``. There are two regular files in this
   tree:

   * ``somefiles/first_file`` - 1337 Bytes
   * ``some_files/deeper_files/second_file`` - 13370 Bytes

   The **total** size of the files in this tree is **1337 + 13370 =
   14707** bytes.

   .. versionadded:: 2.0.0

   By far the simplest way to sum all of the results is using the built-in
   :py:func:`sum` function, or :py:func:`bitmath.sum` for additional control
   (complete docs on that following this section).

   .. code-block:: python

      >>> discovered_files = [f[1] for f in bitmath.listdir('./some_files')]
      >>> print(discovered_files)
      [Byte(1337.0), Byte(13370.0)]
      >>> print(sum(discovered_files))
      14707.0 B
      >>> print(sum(discovered_files).best_prefix())
      14.3623046875 KiB



   Let's call :py:func:`bitmath.listdir` on the ``some_files/``
   directory and see what the results look like. First we'll use all
   the default parameters, then we'll set ``relpath`` to ``True``:

   .. code-block:: python
      :linenos:
      :emphasize-lines: 5-6,10-11

      >>> import bitmath
      >>> for f in bitmath.listdir('./some_files'):
      ...     print(f)
      ...
      ('/tmp/tmp.P5lqtyqwPh/some_files/first_file', Byte(1337.0))
      ('/tmp/tmp.P5lqtyqwPh/some_files/deeper_files/second_file', Byte(13370.0))
      >>> for f in bitmath.listdir('./some_files', relpath=True):
      ...     print(f)
      ...
      ('some_files/first_file', Byte(1337.0))
      ('some_files/deeper_files/second_file', Byte(13370.0))

   On lines **5** and **6** the results print the full path, whereas
   on lines **10** and **11** the path is relative to the present
   working directory.

   Let's play with the ``filter`` parameter now. Let's say we only
   want to include results for files whose name begins with "second":

   .. code-block:: python

      >>> for f in bitmath.listdir('./some_files', filter='second*'):
      ...     print(f)
      ...
      ('/tmp/tmp.P5lqtyqwPh/some_files/deeper_files/second_file', Byte(13370.0))


   If we wish to avoid having to write for-loops, we can collect the
   results into a list rather simply:

   .. code-block:: python

      >>> files = list(bitmath.listdir('./some_files'))
      >>> print(files)
      [('/tmp/tmp.P5lqtyqwPh/some_files/first_file', Byte(1337.0)), ('/tmp/tmp.P5lqtyqwPh/some_files/deeper_files/second_file', Byte(13370.0))]

   Here's a more advanced example where we will sum the size of all
   the returned results and then play around with the possible
   formatting. Recall that a bitmath instance representing the size of
   the discovered file is the second item in each returned tuple.

   .. code-block:: python

      >>> discovered_files = [f[1] for f in bitmath.listdir('./some_files')]
      >>> print(discovered_files)
      [Byte(1337.0), Byte(13370.0)]
      >>> print(reduce(lambda x,y: x+y, discovered_files))
      14707.0 B
      >>> print(reduce(lambda x,y: x+y, discovered_files).best_prefix())
      14.3623046875 KiB
      >>> print(reduce(lambda x,y: x+y, discovered_files).best_prefix().format("{value:.3f} {unit}"))
      14.362 KiB


   .. versionadded:: 1.0.7


.. _bitmath_sum:

bitmath.sum()
=============

.. function:: sum(iterable[, start=None])

   Sum an iterable of bitmath instances into a single bitmath instance.

   :param iterable: Any iterable of bitmath objects to sum.
   :param start: **Default:** ``None`` (accumulates into
                 :class:`bitmath.Byte`). Pass a bitmath instance to
                 set both the starting value and the result type.
   :type start: A bitmath instance, or ``None``
   :returns: A bitmath instance whose type is determined by ``start``
             (or :class:`bitmath.Byte` when ``start`` is ``None``).

   .. note::

      Python's built-in :py:func:`sum` also works with bitmath
      objects. Because ``0 + bm`` returns ``bm`` itself, the built-in
      accumulates into the type of the **first element** in the
      iterable. Use :py:func:`bitmath.sum` instead when you need the
      result normalised to a **specific unit** regardless of the input
      types.

   Sum a homogeneous list — result type matches ``start`` (``Byte`` by
   default):

   .. code-block:: python

      >>> import bitmath
      >>> bitmath.sum([bitmath.MiB(1), bitmath.GiB(1)])
      Byte(1074790400.0)

   Pass ``start`` to choose a different accumulator unit:

   .. code-block:: python

      >>> bitmath.sum([bitmath.KiB(1), bitmath.KiB(2)], start=bitmath.MiB(0))
      MiB(0.0029296875)

   Contrast with the built-in :py:func:`sum`, whose result type tracks the
   first element:

   .. code-block:: python

      >>> sum([bitmath.KiB(1), bitmath.KiB(2)])
      KiB(3.0)
      >>> sum([bitmath.Byte(1), bitmath.MiB(1), bitmath.GiB(1)])
      Byte(1074790401.0)

   .. seealso::

      :ref:`Summing an Iterable <simple_examples_summing>` in *Getting Started*
         Side-by-side examples of built-in :py:func:`sum` vs
         :py:func:`bitmath.sum`.

   .. versionadded:: 2.0.0


bitmath.parse_string()
======================

.. function:: parse_string(str_repr, system=bitmath.NIST, strict=True)

   Parse a string (or, when ``strict=False``, a string or number) into
   a bitmath object.

   :param str_repr: The value to parse. String inputs may include
                    whitespace between the value and the unit.
   :param system: Unit system used when ``strict=False`` and the
                  intended unit cannot be reliably determined from the
                  input. Ignored when ``strict=True``. One of
                  :py:data:`bitmath.NIST` (default) or
                  :py:data:`bitmath.SI`.
   :param strict: When ``True`` (default) the unit must be an exact
                  bitmath type name such as ``"KiB"`` or ``"MB"``.
                  When ``False`` the parser accepts ambiguous input
                  such as plain numbers, numeric strings, and
                  case-insensitive single-letter units. See
                  :ref:`parse-string-non-strict` below.
   :return: A bitmath object representing the input.
   :raises ValueError: if the input cannot be parsed.

   A simple usage example:

   .. code-block:: python

      >>> import bitmath
      >>> a_dvd = bitmath.parse_string("4.7 GiB")
      >>> print(type(a_dvd))
      <class 'bitmath.GiB'>
      >>> print(a_dvd)
      4.7 GiB

   .. caution::

      Caution is advised when reading values from an unverified
      external source such as shell command output or a generated file.
      Many applications (even ``/usr/bin/ls``) do not produce file
      size strings with valid prefix units unless `specially configured
      <https://www.gnu.org/software/coreutils/manual/html_node/Block-size.html#Block-size>`_.
      Use ``strict=False`` for those cases — see :ref:`parse-string-non-strict`.

   To protect your application from unexpected runtime errors, wrap
   calls in a ``try`` statement:

   .. code-block:: python

      >>> import bitmath
      >>> try:
      ...     a_dvd = bitmath.parse_string("4.7 G")
      ... except ValueError:
      ...    print("Error while parsing string into bitmath object")
      ...
      Error while parsing string into bitmath object


   Here are some more examples of valid and invalid input:

   .. code-block:: python

      >>> import bitmath
      >>> sizes = [ 1337, 1337.7, "1337", "1337.7", "1337 B", "1337B" ]
      >>> for size in sizes:
      ...     try:
      ...         print("Parsed size into %s" % bitmath.parse_string(size).best_prefix())
      ...     except ValueError:
      ...         print("Could not parse input: %s" % size)
      ...
      Could not parse input: 1337
      Could not parse input: 1337.7
      Could not parse input: 1337
      Could not parse input: 1337.7
      Parsed size into 1.3056640625 KiB
      Parsed size into 1.3056640625 KiB


   .. versionchanged:: 1.2.4
      Added support for parsing *octet* units via issue `#53 - parse
      french units
      <https://github.com/timlnx/bitmath/issues/53>`_. The `usage
      <https://en.wikipedia.org/wiki/Octet_(computing)#Use>`_ of
      "octet" is still common in some `RFCs
      <https://en.wikipedia.org/wiki/Request_for_Comments>`_, as well
      as France, French Canada and Romania. See also, a table of the
      octet units and their values on `Wikipedia
      <https://en.wikipedia.org/wiki/Octet_(computing)#Unit_multiples>`_.

   Here are some simple examples of parsing *octet* based units:

   .. code-block:: python
      :linenos:
      :emphasize-lines: 4,5

      >>> import bitmath
      >>> a_mebibyte = bitmath.parse_string("1 MiB")
      >>> a_mebioctet = bitmath.parse_string("1 Mio")
      >>> print(a_mebibyte, a_mebioctet)
      1.0 MiB 1.0 MiB
      >>> print(bitmath.parse_string("1Po"))
      1.0 PB
      >>> print(bitmath.parse_string("1337 Eio"))
      1337.0 EiB

   Notice how on lines **4** and **5** the variable ``a_mebibyte``
   from the input ``"1 MiB"`` is exactly equivalent to ``a_mebioctet``
   from ``"1 Mio"``. After parsing, octet units are normalised into
   their standard NIST/SI equivalents automatically.

   .. versionchanged:: 2.0.0
      Added ``strict`` and ``system`` parameters. The default
      ``strict=True`` behavior is identical to earlier versions.
      ``system`` defaults to :py:data:`bitmath.NIST` and is only
      consulted when ``strict=False``.

   .. versionadded:: 1.1.0


.. _parse-string-non-strict:

parse_string with ``strict=False``
-----------------------------------

When ``strict=False`` the parser accepts ambiguous input that does not
conform to exact bitmath type names — for example, the single-letter
units produced by tools like ``ls -h``, ``df``, and ``qemu-img``. This
is the behavior previously provided by the now-deprecated
:py:func:`bitmath.parse_string_unsafe`.

All inputs are treated as **byte-based**. Bit-based units are not
supported in non-strict parsing mode. Capitalisation does not matter.

.. _parse-string-system-hint:

Understanding the ``system`` parameter in non-strict mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

   In ``strict=False`` mode, ``system`` is a **tiebreaker**, not a
   guarantee. It is only consulted when the parser cannot determine the
   unit system from the input itself. Passing ``system=bitmath.SI``
   does **not** force all results to be SI units.

The parser resolves the unit system in the following order of
precedence:

1. **No unit present** — plain numbers and numeric strings (e.g.
   ``100``, ``"2048"``) are always returned as :class:`bitmath.Byte`
   regardless of ``system``.

2. **Unit is self-describing** — inputs whose unit already contains an
   ``i`` marker (e.g. ``"100 KiB"``, ``"4Gi"``) unambiguously identify
   a NIST unit. ``system`` is ignored and the result is always NIST.

3. **Unit is ambiguous** — single-letter units such as ``k``, ``M``,
   ``G`` carry no inherent system information. Only here does
   ``system`` act as the deciding hint: ``system=bitmath.NIST``
   (the default) interprets ``"4G"`` as ``GiB(4)``; passing
   ``system=bitmath.SI`` interprets it as ``GB(4)``.

In summary: ``system`` resolves ambiguity — it does not override
evidence already present in the input string.

In this example we parse the output of ``df -H / /boot /home``,
whose ``Used`` column contains single-letter SI units. Because the
units are ambiguous we pass ``system=bitmath.SI`` as a hint::

   Filesystem                                 Size  Used Avail Use% Mounted on
   /dev/mapper/luks-ca8d5493-72bb-4691-afe1   107G   64G   38G  63% /
   /dev/sda1                                  500M  391M   78M  84% /boot
   /dev/mapper/vg_deepfryer-lv_home           129G  118G  4.7G  97% /home

.. code-block:: python
   :linenos:
   :emphasize-lines: 7

   >>> with open('/tmp/df-output.txt', 'r') as fp:
   ...     _ = fp.readline()   # skip header
   ...     for line in fp.readlines():
   ...         cols = line.split()[0:4]
   ...         print("""Filesystem: %s
   ... - Used: %s""" % (cols[0],
   ...             bitmath.parse_string(cols[1], strict=False, system=bitmath.SI)))
   Filesystem: /dev/mapper/luks-ca8d5493-72bb-4691-afe1
   - Used: 107.0 GB
   Filesystem: /dev/sda1
   - Used: 500.0 MB
   Filesystem: /dev/mapper/vg_deepfryer-lv_home
   - Used: 129.0 GB

If ``df`` is run with ``-h`` instead of ``-H`` it produces NIST-sized
values but still prints the same single-letter units. Omit ``system``
(NIST is the default) or pass ``system=bitmath.NIST`` explicitly:

.. code-block:: python
   :linenos:
   :emphasize-lines: 7

   >>> with open('/tmp/df-output.txt', 'r') as fp:
   ...     _ = fp.readline()   # skip header
   ...     for line in fp.readlines():
   ...         cols = line.split()[0:4]
   ...         print("""Filesystem: %s
   ... - Used: %s""" % (cols[0],
   ...             bitmath.parse_string(cols[1], strict=False, system=bitmath.NIST)))
   Filesystem: /dev/mapper/luks-ca8d5493-72bb-4691-afe1
   - Used: 100.0 GiB
   Filesystem: /dev/sda1
   - Used: 477.0 MiB
   Filesystem: /dev/mapper/vg_deepfryer-lv_home
   - Used: 120.0 GiB

The results now use the proper NIST prefix syntax: ``GiB``.


bitmath.parse_string_unsafe()
=============================

.. deprecated:: 2.0.0

   ``parse_string_unsafe`` is deprecated and will be removed in a
   future release. Use :py:func:`bitmath.parse_string` with
   ``strict=False`` instead:

   .. code-block:: python

      # old
      bitmath.parse_string_unsafe(value, system=bitmath.NIST)

      # new
      bitmath.parse_string(value, strict=False, system=bitmath.NIST)

   To suppress the deprecation warning in the interim:

   .. code-block:: python

      import warnings
      warnings.filterwarnings('ignore', category=DeprecationWarning,
                              module='bitmath')

.. function:: parse_string_unsafe(repr[, system=bitmath.NIST])

   A deprecated thin wrapper around
   ``parse_string(repr, strict=False, system=system)``. All behavior,
   parameters, and caveats are identical to
   :ref:`parse_string with strict=False <parse-string-non-strict>`.

   :param repr: The value to parse.
   :param system: :py:data:`bitmath.NIST` (default) or
                  :py:data:`bitmath.SI`.
   :return: A bitmath object representing ``repr``.
   :raises ValueError: if ``repr`` cannot be parsed.

   .. versionchanged:: 2.0.0
      Deprecated. Default ``system`` changed from ``bitmath.SI`` to
      ``bitmath.NIST`` for consistency with
      :py:func:`bitmath.parse_string`.

   .. versionadded:: 1.3.1


bitmath.query_device_capacity()
===============================

.. function:: query_device_capacity(device_fd)

   Create :class:`bitmath.Byte` instances representing the capacity of
   a block device.

   :param file device_fd: An open file handle (``handle =
                          open('/dev/sda')``) of the target device.
   :return: A :class:`bitmath.Byte` equal to the size of ``device_fd``.
   :raises ValueError: if file descriptor ``device_fd`` is not of a
                       device type.
   :raises IOError:

      * :py:exc:`IOError[13]` - If the effective **uid** of this
        process does not have access to issue raw commands to block
        devices. I.e., this process does not have super-user rights.
      * :py:exc:`IOError[2]` - If the device ``device_fd`` points to
        does not exist.


   .. include:: query_device_capacity_warning.rst


   .. include:: example_block_devices.rst


   Here's an example using the ``with`` context manager to open a
   device and print its capacity with the best-human readable prefix
   (line **3**):

   .. code-block:: python
      :linenos:
      :emphasize-lines: 3

      >>> import bitmath
      >>> with open("/dev/sda") as device:
      ...     size = bitmath.query_device_capacity(device).best_prefix()
      ...     print("Device %s capacity: %s (%s Bytes)" % (device.name, size, size_bytes))
      Device /dev/sda capacity: 238.474937439 GiB (2.56060514304e+11 Bytes)


   :raises NotImplementedError: if called on an unsupported platform.
                               Supported platforms are Linux, macOS,
                               and Windows.

   .. note:: **Windows usage**: open the device as
             ``open(r'\\.\PhysicalDrive0', 'rb')`` (administrator
             privileges required).  The device path must start with
             ``\\.\`` — passing a regular file path raises
             :py:exc:`ValueError`.

   .. versionadded:: 1.2.4

.. _module_context_managers:

Context Managers
****************

This section describes all of the `context managers
<https://docs.python.org/3/reference/datamodel.html#context-managers>`_
provided by the bitmath class.

.. warning::

   It is a known limitation that the bitmath context managers are
   **not thread-safe**. You may get unexpected results or errors using
   these in a threaded environment.

   The suggested workaround is to apply formatting to each object
   instance directly. See the instance :ref:`format
   <instances_format>` method docs for additional reference.


.. note::

   For a bit of background, a *context manager* (specifically, the
   ``with`` statement) is a feature of the Python language which is
   commonly used to:

   * Decorate, or *wrap*, an arbitrary block of code. I.e., effect a
     certain condition onto a specific body of code

   * Automatically *open* and *close* an object which is used in a
     specific context. I.e., handle set-up and tear-down of objects in
     the place they are used.

.. seealso::

   :pep:`343`
      *The "with" Statement*

   :pep:`318`
      *Decorators for Functions and Methods*


.. _module_bitmath_format:

bitmath.format()
================

.. function:: format([fmt_str=None[, plural=False[, bestprefix=False]]])

   The :py:func:`bitmath.format` context manager allows you to specify
   the string representation of all bitmath instances within a
   specific block of code.

   This is effectively equivalent to applying the
   :ref:`format()<instances_format>` method to an entire region of
   code.

   :param str fmt_str: a formatting mini-language compat formatting
                       string. See the :ref:`instance attributes
                       <instances_attributes>` for a list of available
                       items.
   :param bool plural: ``True`` enables printing instances with
                       trailing **s**'s if they're plural. ``False``
                       (default) prints them as singular (no trailing
                       's')
   :param bool bestprefix: ``True`` enables printing instances in
                           their best human-readable
                           representation. ``False``, the default,
                           prints instances using their current prefix
                           unit.


   .. note:: The ``bestprefix`` parameter is not yet implemented!

   Let's look at an example of toggling pluralization on and
   off. First we'll look over a demonstration script (below), and then
   we'll review the output.

   .. code-block:: python
      :linenos:
      :emphasize-lines: 33-34

      import bitmath

      a_single_bit = bitmath.Bit(1)
      technically_plural_bytes = bitmath.Byte(0)
      always_plural_kbs = bitmath.kb(42)

      formatting_args = {
          'not_plural': a_single_bit,
          'technically_plural': technically_plural_bytes,
          'always_plural': always_plural_kbs
      }

      print("""None of the following will be pluralized, because that feature is turned off
      """)

      test_string = """   One unit of 'Bit': {not_plural}

         0 of a unit is typically said pluralized in US English: {technically_plural}

         several items of a unit will always be pluralized in normal US English
         speech: {always_plural}"""

      print(test_string.format(**formatting_args))

      print("""
      ----------------------------------------------------------------------
      """)

      print("""Now, we'll use the bitmath.format() context manager
      to print the same test string, but with pluralization enabled.
      """)

      with bitmath.format(plural=True):
          print(test_string.format(**formatting_args))

   The context manager is demonstrated in lines **33** → **34**. In
   these lines we use the :py:func:`bitmath.format` context manager,
   setting ``plural`` to ``True``, to print the original string
   again. By doing this we have enabled pluralized string
   representations (where appropriate). Running this script would have
   the following output::


      None of the following will be pluralized, because that feature is turned off

         One unit of 'Bit': 1.0 b

         0 of a unit is typically said pluralized in US English: 0.0 B

         several items of a unit will always be pluralized in normal US English
         speech: 42.0 kb

      ----------------------------------------------------------------------

      Now, we'll use the bitmath.format() context manager
      to print the same test string, but with pluralization enabled.

         One unit of 'Bit': 1.0 b

         0 of a unit is typically said pluralized in US English: 0.0 B

         several items of a unit will always be pluralized in normal US English
         speech: 42.0 kbs

   Here's a shorter example, where we'll:

   * Print a string containing bitmath instances using the default
     formatting (lines **2** → **3**)
   * Use the context manager to print the instances in scientific
     notation (lines **4** → **7**)
   * Print the string one last time to demonstrate how the formatting
     automatically returns to the default format (lines **8** → **9**)

   .. code-block:: python
      :linenos:

      >>> import bitmath
      >>> print("Some instances: %s, %s" % (bitmath.KiB(1 / 3.0), bitmath.Bit(512)))
      Some instances: 0.333333333333 KiB, 512.0 b
      >>> with bitmath.format("{value:e}-{unit}"):
      ...     print("Some instances: %s, %s" % (bitmath.KiB(1 / 3.0), bitmath.Bit(512)))
      ...
      Some instances: 3.333333e-01-KiB, 5.120000e+02-b
      >>> print("Some instances: %s, %s" % (bitmath.KiB(1 / 3.0), bitmath.Bit(512)))
      Some instances: 0.333333333333 KiB, 512.0 b


   .. versionadded:: 1.0.8


.. _module_class_variables:

Module Variables
****************

This section describes the module-level variables. Some of which are
constants and are used for reference. Some of which effect output or
behavior.

.. versionchanged:: 1.0.7
   The formatting strings were not available for manupulate/inspection
   in earlier versions

.. versionadded:: 1.1.1
   Prior to this version :py:data:`ALL_UNIT_TYPES` was not defined

.. note:: Modifying these variables will change the default
          representation indefinitely. Use the
          :py:func:`bitmath.format` context manager to limit
          changes to a specific block of code.

.. _module_format_string:

.. py:data:: format_string

   This is the default string representation of all bitmath
   instances. The default value is ``{value} {unit}`` which, when
   evaluated, formats an instance as a floating point number with at
   least one digit of precision, followed by a character of
   whitespace, followed by the prefix unit of the instance.

   For example, given bitmath instances representing the following
   values: **1337 MiB**, **0.1234567 kb**, and **0 B**, their printed
   output would look like the following:

   .. code-block:: python

      >>> from bitmath import *
      >>> print(MiB(1337), kb(0.1234567), Byte(0))
      1337.0 MiB 0.1234567 kb 0.0 B

   We can make these instances print however we want to. Let's wrap
   each one in square brackets (``[``, ``]``), replace the separating
   space character with a hyphen (``-``), and limit the precision to
   just 2 digits:

   .. code-block:: python

      >>> import bitmath
      >>> bitmath.format_string = "[{value:.2f}-{unit}]"
      >>> print(bitmath.MiB(1337), bitmath.kb(0.1234567), bitmath.Byte(0))
      [1337.00-MiB] [0.12-kb] [0.00-Byte]

.. py:data:: format_plural

   A boolean which controls the pluralization of instances in string
   representation. The default is ``False``.

   If we wanted to enable pluralization we could set the
   :py:data:`format_plural` variable to ``True``. First, let's look at
   some output using the default singular formatting.

   .. code-block:: python

      >>> import bitmath
      >>> print(bitmath.MiB(1337))
      1337.0 MiB

   And now we'll enable pluralization (line **2**):

   .. code-block:: python
      :linenos:
      :emphasize-lines: 2,5

      >>> import bitmath
      >>> bitmath.format_plural = True
      >>> print(bitmath.MiB(1337))
      1337.0 MiBs
      >>> bitmath.format_plural = False
      >>> print(bitmath.MiB(1337))
      1337.0 MiB

   On line **5** we disable pluralization again and then see that the
   output has no trailing "s" character.

.. py:data:: NIST

   Constant used as an argument to some functions to specify the
   **NIST** system.

.. py:data:: SI

   Constant used as an argument to some functions to specify the
   **SI** system.

.. py:data:: SI_PREFIXES

   An array of all of the SI unit prefixes (e.g., ``k``, ``M``, or
   ``E``)

.. py:data:: SI_STEPS

   .. code-block:: python

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


.. py:data:: NIST_PREFIXES

   An array of all of the NIST unit prefixes (e.g., ``Ki``, ``Mi``, or
   ``Ei``)


.. py:data:: NIST_STEPS

   .. code-block:: python

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


.. py:data:: ALL_UNIT_TYPES

   An array of all combinations of known valid prefix units mixed with
   both bit and byte suffixes.

   .. code-block:: python

      ALL_UNIT_TYPES = ['Bit', 'Byte', 'kb', 'kB', 'Mb', 'MB', 'Gb', 'GB',
         'Tb', 'TB', 'Pb', 'PB', 'Eb', 'EB', 'Zb', 'ZB', 'Yb', 'YB',
         'Kib', 'KiB', 'Mib', 'MiB', 'Gib', 'GiB', 'Tib', 'TiB',
         'Pib', 'PiB', 'Eib', 'EiB', 'Zib', 'ZiB', 'Yib', 'YiB']

.. _bitmath_3rd_party_module_integrations:

3rd Party Module Integrations
*****************************

Self-contained, copy-paste examples for integrating :mod:`bitmath` with
:mod:`argparse`, `click <https://click.palletsprojects.com/>`_, and
`progressbar2 <https://progressbar-2.readthedocs.io/>`_ are collected in
the :ref:`Integration Examples <integration_examples>` chapter.
