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
| Division       | ``bm`` / ``num``  | ``type(bm)``        | ``KiB(1) / 3`` = ``0.3330078125KiB``  |
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
<https://docs.python.org/2.7/reference/datamodel.html#basic-customization>`_
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
   [KiB(7892.0), KiB(7337.0), KiB(4190.0), KiB(4003.0), KiB(2326.0), KiB(2178.0), KiB(2126.0), KiB(1770.0), KiB(1441.0), KiB(48.0)]
