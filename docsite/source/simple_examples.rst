Getting Started
###############

In this section we will take a high-level look at the basic things you
can do with bitmath. We'll include the following topics:

.. contents::
   :depth: 3
   :local:


.. _simple_examples_supported_operations:

Tables of Supported Operations
******************************

The following legend describes the two operands used in the tables below.

=======  =======================================
Operand  Description
=======  =======================================
``bm``   A bitmath object is required
``num``  An integer or decimal value is required
=======  =======================================


.. _getting_started_arithmetic:

Arithmetic
==========

Math works mostly like you expect it to, except for a few edge-cases:

* Mixing bitmath types with Number types (the result varies
  per-operation)

* Operations where two bitmath types would cancel out (such as
  dividing two bitmath types)

* Multiplying two bitmath instances together is supported, but the
  results may not make much sense.


.. seealso::

   :ref:`Appendix: Rules for Math <appendix_math>`
      For a discussion of the behavior of bitmath and number types.


.. _simple_examples_arithmetic_table:

+----------------+-------------------+---------------------+---------------------------------------+
| Operation      | Parameters        | Result Type         | Example                               |
+================+===================+=====================+=======================================+
| Addition       | ``bm1`` + ``bm2`` | ``type(bm1)``       | ``KiB(1) + MiB(2)`` = ``2049.0KiB``   |
+----------------+-------------------+---------------------+---------------------------------------+
| Addition       | ``bm`` + ``num``  | ``type(num)``       | ``KiB(1) + 1`` = ``2.0``              |
+----------------+-------------------+---------------------+---------------------------------------+
| Addition       | ``num`` + ``bm``  | ``type(num)``       | ``1 + KiB(1)`` = ``2.0``              |
+----------------+-------------------+---------------------+---------------------------------------+
| Subtraction    | ``bm1`` - ``bm2`` | ``type(bm1)``       | ``KiB(1) - Byte(2048)`` = ``-1.0KiB`` |
+----------------+-------------------+---------------------+---------------------------------------+
| Subtraction    | ``bm`` - ``num``  | ``type(num)``       | ``KiB(4) - 1`` = ``3.0``              |
+----------------+-------------------+---------------------+---------------------------------------+
| Subtraction    | ``num`` - ``bm``  | ``type(num)``       | ``10 - KiB(1)`` = ``9.0``             |
+----------------+-------------------+---------------------+---------------------------------------+
| Multiplication | ``bm1`` * ``bm2`` | ``type(bm1)``       | ``KiB(1) * KiB(2)`` = ``2048.0KiB``   |
+----------------+-------------------+---------------------+---------------------------------------+
| Multiplication | ``bm`` * ``num``  | ``type(bm)``        | ``KiB(2) * 3`` = ``6.0KiB``           |
+----------------+-------------------+---------------------+---------------------------------------+
| Multiplication | ``num`` * ``bm``  | ``type(bm)``        | ``2 * KiB(3)`` = ``6.0KiB``           |
+----------------+-------------------+---------------------+---------------------------------------+
| Division       | ``bm1`` / ``bm2`` | ``type(num)``       | ``KiB(1) / KiB(2)`` = ``0.5``         |
+----------------+-------------------+---------------------+---------------------------------------+
| Division       | ``bm`` / ``num``  | ``type(bm)``        | ``KiB(6) / 4`` = ``KiB(1.5)``         |
+----------------+-------------------+---------------------+---------------------------------------+
| Division       | ``num`` / ``bm``  | ``type(num)``       | ``3 / KiB(2)`` = ``1.5``              |
+----------------+-------------------+---------------------+---------------------------------------+


Bitwise Operations
==================

.. seealso::

   `Bitwise Calculator <http://www.miniwebtool.com/bitwise-calculator/>`_
      A free online calculator for checking your math

Bitwise operations are also supported. Bitwise operations work
directly on the ``bits`` attribute of a bitmath instance, not the
number you see in an instances printed representation (``value``), to
maintain accuracy.

+----------------+-----------------------+--------------+---------------------------------------------------------+
| Operation      | Parameters            | Result Type  | Example\ :sup:`1`                                       |
+================+=======================+==============+=========================================================+
| Left Shift     | ``bm`` << ``num``     | ``type(bm)`` | ``MiB(1)`` << ``2`` = ``MiB(4.0)``                      |
+----------------+-----------------------+--------------+---------------------------------------------------------+
| Right Shift    | ``bm`` >> ``num``     | ``type(bm)`` | ``MiB(1)`` >> ``2`` = ``MiB(0.25)``                     |
+----------------+-----------------------+--------------+---------------------------------------------------------+
| AND            | ``bm`` & ``num``      | ``type(bm)`` | ``MiB(13.37)`` & ``1337`` = ``MiB(0.000126...)``        |
+----------------+-----------------------+--------------+---------------------------------------------------------+
| OR             | ``bm`` \|     ``num`` | ``type(bm)`` | ``MiB(13.37)`` \|     ``1337`` = ``MiB(13.3700...)``    |
+----------------+-----------------------+--------------+---------------------------------------------------------+
| XOR            | ``bm`` ^ ``num``      | ``type(bm)`` | ``MiB(13.37)`` ^ ``1337`` = ``MiB(13.369...)``          |
+----------------+-----------------------+--------------+---------------------------------------------------------+

1. *Give me a break here, it's not easy coming up with compelling examples for bitwise operations...*


Basic Math
**********

bitmath supports all arithmetic operations

.. code-block:: python
   :linenos:

   >>> eighty_four_mib = fourty_two_mib + fourty_two_mib_in_kib
   >>> eighty_four_mib
   MiB(84.00)
   >>> eighty_four_mib == fourty_two_mib * 2
   True


Unit Conversion
***************

.. code-block:: python
   :linenos:

   >>> from bitmath import *
   >>> fourty_two_mib = MiB(42)
   >>> fourty_two_mib_in_kib = fourty_two_mib.to_KiB()
   >>> fourty_two_mib_in_kib
   KiB(43008.00)

   >>> fourty_two_mib
   MiB(42.00)

   >>> fourty_two_mib.KiB
   KiB(43008.00)

Rich Comparison
***************

Rich Comparison (as per the `Python Basic Customization
<https://docs.python.org/3/reference/datamodel.html#basic-customization>`_
magic methods) ``<``, ``<=``, ``==``, ``!=``, ``>``, ``>=`` is fully
supported:

.. code-block:: python
   :linenos:

   >>> GB(1) < GiB(1)
   True
   >>> GB(1.073741824) == GiB(1)
   True
   >>> GB(1.073741824) <= GiB(1)
   True
   >>> Bit(1) == TiB(bits=1)
   True
   >>> kB(100) > EiB(bytes=1024)
   True
   >>> kB(100) >= EiB.from_other(kB(100))
   True
   >>> kB(100) >= EiB.from_other(kB(99))
   True
   >>> kB(100) >= EiB.from_other(kB(9999))
   False
   >>> KiB(100) != Byte(1)
   True


Sorting
*******

bitmath natively supports sorting.

Let's make a list of the size (in bytes) of all the files in the
present working directory (lines **4** and **5**) and then print them
out sorted by increasing magnitude (lines **10** and **11**, and
**13** → **15**):

.. code-block:: python
   :linenos:
   :emphasize-lines: 4,5,10,11,13,14,15

   >>> from bitmath import *
   >>> import os
   >>> sizes = []
   >>> for f in os.listdir('./tests/'):
   ...     sizes.append(KiB(os.path.getsize('./tests/' + f)))

   >>> print(sizes)
   [KiB(7337.00), KiB(1441.00), KiB(2126.00), KiB(2178.00), KiB(2326.00), KiB(4003.00), KiB(48.00), KiB(1770.00), KiB(7892.00), KiB(4190.00)]

   >>> print(sorted(sizes))
   [KiB(48.00), KiB(1441.00), KiB(1770.00), KiB(2126.00), KiB(2178.00), KiB(2326.00), KiB(4003.00), KiB(4190.00), KiB(7337.00), KiB(7892.00)]

   >>> human_sizes = [s.best_prefix() for s in sizes]
   >>> print(sorted(human_sizes))
   [KiB(48.00), MiB(1.41), MiB(1.73), MiB(2.08), MiB(2.13), MiB(2.27), MiB(3.91), MiB(4.09), MiB(7.17), MiB(7.71)]

Now print them out in descending magnitude

.. code-block:: python

   >>> print(sorted(human_sizes, reverse=True))
   [MiB(7.71), MiB(7.17), MiB(4.09), MiB(3.91), MiB(2.27), MiB(2.13), MiB(2.08), MiB(1.73), MiB(1.41), KiB(48.00)]


Parsing Strings
***************

:py:func:`bitmath.parse_string` converts a human-readable string into
a bitmath instance. By default the unit must be an exact bitmath type
name:

.. code-block:: python

   >>> import bitmath
   >>> bitmath.parse_string("4.7 GiB")
   GiB(4.70)
   >>> bitmath.parse_string("1337 MB")
   MB(1337.00)
   >>> bitmath.parse_string("1 Mio")   # octet alias
   MiB(1.00)

When the input comes from a tool that produces ambiguous output
(often-times single-letter units) use ``strict=False``. Pass
``system=bitmath.SI`` or ``system=bitmath.NIST`` to tell the parser
which system to use if the unit can not reliably be determined
automatically:

.. code-block:: python

   >>> bitmath.parse_string("4G", strict=False)             # NIST default
   GiB(4.00)
   >>> bitmath.parse_string("4G", strict=False, system=bitmath.SI)
   GB(4.00)
   >>> bitmath.parse_string("100", strict=False)            # plain number → bytes
   Byte(100.00)
   >>> bitmath.parse_string("100 GiB", strict=False, system=bitmath.SI)  # i-marker wins
   GiB(100.00)

.. seealso::

   :py:func:`bitmath.parse_string` — full parameter reference and caveats.


.. _simple_examples_summing:

Summing an Iterable
*******************

The built-in :py:func:`sum` works with bitmath objects. Because
``0 + bm`` returns ``bm`` itself (the identity element), accumulation
starts correctly and the result type matches the **first element** in
the iterable:

.. code-block:: python

   >>> import bitmath
   >>> sum([bitmath.KiB(1), bitmath.KiB(2)])
   KiB(3.00)
   >>> sum([bitmath.Byte(1), bitmath.MiB(1), bitmath.GiB(1)])
   Byte(1074790401.00)

Results from mixing plain numbers and numbers with units yields a
result with no units.

.. code-block:: python

   >>> sum([bitmath.Byte(1), 0])
   1.0
   >>> sum([1, bitmath.KiB(2)])
   3.0

.. seealso::

   :ref:`Appendix: Rules for Math <appendix_math_mixed_types>` — for a
   thrilling discussion about the minute details when doing mixed-type
   math math. What it all boils down to is this: if we don’t provide a
   unit then bitmath won’t give us one back.


Use :py:func:`bitmath.sum` when you need the result **normalised to a
specific unit** regardless of the input types. Without a ``start``
argument it accumulates into :class:`bitmath.Byte`; pass ``start`` to
choose a different accumulator (resultant unit):

.. code-block:: python

   >>> bitmath.sum([bitmath.MiB(1), bitmath.GiB(1)])
   Byte(1074790400.00)
   >>> bitmath.sum([bitmath.KiB(1), bitmath.KiB(2)], start=bitmath.MiB(0))
   MiB(0.00)
   >>> bitmath.sum([bitmath.MiB(100), bitmath.KiB(2000)], start=bitmath.GiB(0))
   GiB(0.10)

Rounding
********

bitmath represents sizes as floating-point measurements. When an integer
result is needed, Python's :py:func:`math.floor`, :py:func:`math.ceil`,
and :py:func:`round` all work directly on bitmath instances and return
an instance of the same type:

.. code-block:: python

   >>> import math, bitmath
   >>> math.floor(bitmath.KiB(1) / 3)
   KiB(0)
   >>> math.ceil(bitmath.KiB(1) / 3)
   KiB(1)
   >>> round(bitmath.MiB(1.75))
   MiB(2)
   >>> round(bitmath.GiB(1.23456), 2)
   GiB(1.23)

.. warning::

   Rounding intermediate results is lossy. ``math.floor(GiB(10) / 3) * 3``
   yields ``GiB(9)``, not ``GiB(10)``. Only round at the final output step.

.. seealso::

   :ref:`Appendix: Rules for Math <appendix_math>` — discussion of
   floating-point representation and when rounding is appropriate.


Choosing a Formatting Approach
******************************

bitmath offers several ways to control how instances are rendered as
strings. They overlap deliberately — each suits a different situation.
This section helps you pick the right one.

**Quick reference**

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Approach
     - Best for
     - Avoid when
   * - Default ``str()``
     - Printing, debugging, logging
     - You need custom precision or layout
   * - ``instance.format()``
     - Full control over layout using any instance attribute
     - You only need to format the number
   * - f-strings / ``format()``
     - Inline formatting in modern Python; columnar output
     - You need unit-aware attributes beyond ``value``
   * - ``bitmath.format()`` context manager
     - Consistent formatting across a block of code; threaded code
     - A one-off format on a single value
   * - ``bitmath.format_string`` global
     - Changing the default for an entire script or session
     - Anything other than a top-level script (mutates global state)

Default ``str()``
=================

The simplest option. Just print or convert to string — no imports, no
setup. Output follows the module-level ``format_string`` (default:
``"{value:.2f} {unit}"``):

.. code-block:: python

   >>> import bitmath
   >>> print(bitmath.MiB(1.5))
   1.50 MiB
   >>> str(bitmath.GiB(10))
   '10.00 GiB'

**Use this when** you just need a readable value and don't care about
precision or alignment.

``instance.format()``
=====================

The most expressive option. The format string has access to every
instance attribute — ``{value}``, ``{unit}``, ``{bits}``, ``{bytes}``,
``{system}``, ``{base}``, ``{power}``, and more:

.. code-block:: python

   >>> size = bitmath.MiB(1 / 3.0)
   >>> size.format("{value:.2f} {unit} ({bits:.0f} bits)")
   '0.33 MiB (2796202 bits)'

**Use this when** you need the unit label, bit/byte counts, or any
other instance attribute woven into the output string.

.. seealso::

   :ref:`Instance Formatting <instances_format>` — full attribute reference.

f-strings and ``format()``
===========================

Standard Python formatting. The format spec applies to ``self.value``
only; the unit is omitted unless you add it explicitly with
``{size.unit}``:

.. code-block:: python

   >>> size = bitmath.GiB(127.3)
   >>> f'{size:.2f} {size.unit}'
   '127.30 GiB'
   >>> f'{size}'           # no spec → same as str(size)
   '127.30 GiB'

This shines for columnar output where alignment matters:

.. code-block:: python

   >>> rows = [("home", bitmath.GiB(127.3)), ("tmp", bitmath.MiB(843.7))]
   >>> for mount, size in rows:
   ...     print(f"{mount:<8} {size:>10.2f} {size.unit}")
   home        127.30 GiB
   tmp         843.70 MiB

**Use this when** you're building formatted strings inline and only
need the numeric value with a precision or alignment spec.

``bitmath.format()`` context manager
=====================================

Sets ``fmt_str``, ``plural``, and ``bestprefix`` for every bitmath
``str()`` call within the block, then restores the previous state
automatically — even if an exception is raised. Safe to use in
threaded code:

.. code-block:: python

   >>> sizes = [bitmath.KiB(1024), bitmath.MiB(512)]
   >>> with bitmath.format(fmt_str="{value:.1f} {unit}", bestprefix=True):
   ...     for s in sizes:
   ...         print(s)
   1.0 MiB
   512.0 MiB

**Use this when** you want a consistent format across multiple
``print()`` or ``str()`` calls without touching each one individually,
or when you're in a threaded environment.

.. seealso::

   :ref:`bitmath.format() <module_bitmath_format>` — full parameter reference.

``bitmath.format_string`` global
=================================

Sets the default representation for *all* bitmath instances for the
remainder of the process. Useful at the top of a script; a poor choice
inside a library or threaded code:

.. code-block:: python

   >>> import bitmath
   >>> bitmath.format_string = "{value:.2f} {unit}"
   >>> print(bitmath.MiB(1.5))
   1.50 MiB

**Use this when** you control the entire script and want a single
format everywhere without wrapping everything in a context manager.
Prefer the context manager for anything more targeted.

.. warning::

   Mutating ``bitmath.format_string`` directly affects all threads.
   Use the :py:func:`bitmath.format` context manager instead in
   concurrent code.
