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
   MiB(84.0)
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
   KiB(43008.0)

   >>> fourty_two_mib
   MiB(42.0)

   >>> fourty_two_mib.KiB
   KiB(43008.0)

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
   [KiB(7337.0), KiB(1441.0), KiB(2126.0), KiB(2178.0), KiB(2326.0), KiB(4003.0), KiB(48.0), KiB(1770.0), KiB(7892.0), KiB(4190.0)]

   >>> print(sorted(sizes))
   [KiB(48.0), KiB(1441.0), KiB(1770.0), KiB(2126.0), KiB(2178.0), KiB(2326.0), KiB(4003.0), KiB(4190.0), KiB(7337.0), KiB(7892.0)]

   >>> human_sizes = [s.best_prefix() for s in sizes]
   >>> print(sorted(human_sizes))
   [KiB(48.0), MiB(1.4072265625), MiB(1.728515625), MiB(2.076171875), MiB(2.126953125), MiB(2.271484375), MiB(3.9091796875), MiB(4.091796875), MiB(7.1650390625), MiB(7.70703125)]

Now print them out in descending magnitude

.. code-block:: python

   >>> print(sorted(human_sizes, reverse=True))
   [MiB(7.70703125), MiB(7.1650390625), MiB(4.091796875), MiB(3.9091796875), MiB(2.271484375), MiB(2.126953125), MiB(2.076171875), MiB(1.728515625), MiB(1.4072265625), KiB(48.0)]


Parsing Strings
***************

:py:func:`bitmath.parse_string` converts a human-readable string into
a bitmath instance. By default the unit must be an exact bitmath type
name:

.. code-block:: python

   >>> import bitmath
   >>> bitmath.parse_string("4.7 GiB")
   GiB(4.7)
   >>> bitmath.parse_string("1337 MB")
   MB(1337.0)
   >>> bitmath.parse_string("1 Mio")   # octet alias
   MiB(1.0)

When the input comes from a tool that produces ambiguous output
(often-times single-letter units) use ``strict=False``. Pass
``system=bitmath.SI`` or ``system=bitmath.NIST`` to tell the parser
which system to use if the unit can not reliably be determined
automatically:

.. code-block:: python

   >>> bitmath.parse_string("4G", strict=False)             # NIST default
   GiB(4.0)
   >>> bitmath.parse_string("4G", strict=False, system=bitmath.SI)
   GB(4.0)
   >>> bitmath.parse_string("100", strict=False)            # plain number → bytes
   Byte(100.0)
   >>> bitmath.parse_string("100 GiB", strict=False, system=bitmath.SI)  # i-marker wins
   GiB(100.0)

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
   KiB(3.0)
   >>> sum([bitmath.Byte(1), bitmath.MiB(1), bitmath.GiB(1)])
   Byte(1074790401.0)

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
   Byte(1074790400.0)
   >>> bitmath.sum([bitmath.KiB(1), bitmath.KiB(2)], start=bitmath.MiB(0))
   MiB(0.0029296875)
   >>> bitmath.sum([bitmath.MiB(100), bitmath.KiB(2000)], start=bitmath.GiB(0))
   GiB(0.0995635986328125)

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
