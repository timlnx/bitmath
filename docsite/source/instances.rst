Instances
#########

.. _instance_attributes:

.. contents::
   :depth: 3
   :local:


.. _instances_attributes:

Instance Attributes
*******************

bitmath objects have several instance attributes:

.. py:attribute:: BitMathInstance.base

   The mathematical base of the unit of the instance (this will be **2** or **10**)

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.base
      2

.. py:attribute:: BitMathInstance.binary

   The `Python binary representation
   <https://docs.python.org/3/library/functions.html#bin>`_ of the
   instance's value (in bits)

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.binary
      0b10100111001000

.. py:attribute:: BitMathInstance.bin

   This is an alias for ``binary``

.. py:attribute:: BitMathInstance.bits

   The number of bits in the object

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.bits
      10696.0

.. py:attribute:: BitMathInstance.bytes

   The number of bytes in the object

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.bytes
      1337

.. py:attribute:: BitMathInstance.power

   The mathematical power the ``base`` of the unit of the instance is raised to

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.power
      0

.. py:attribute:: BitMathInstance.system

   The system of units used to measure this instance (``NIST`` or ``SI``)

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.system
      NIST

.. py:attribute:: BitMathInstance.value

   The value of the instance in *prefix* units\ :sup:`1`

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.value
      1337.0

.. py:attribute:: BitMathInstance.unit

   The string representation of this prefix unit (such as ``MiB`` or ``kb``)

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.unit
      Byte

.. py:attribute:: BitMathInstance.unit_plural

   The pluralized string representation of this prefix unit.

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.unit_plural
      Bytes

.. py:attribute:: BitMathInstance.unit_singular

   The singular string representation of this prefix unit (such as
   ``MiB`` or ``kb``)

   .. code-block:: python

      >>> b = bitmath.Byte(1337)
      >>> print b.unit_singular
      Byte


**Notes:**

1. Given an instance ``k``, where ``k = KiB(1.3)``, then ``k.value`` is **1.3**

----

The following is an example of how to access some of these attributes
and what you can expect their printed representation to look like:

.. code-block:: python
   :linenos:

   >>> dvd_capacity = GB(4.7)
   >>> print "Capacity in bits: %s\nbytes: %s\n" % \
                (dvd_capacity.bits, dvd_capacity.bytes)

   Capacity in bits: 37600000000.0
   bytes: 4700000000.0

   >>> dvd_capacity.value
   4.7

   >>> dvd_capacity.bin
   '0b100011000001001000100111100000000000'

   >>> dvd_capacity.binary
   '0b100011000001001000100111100000000000'



Instance Methods
****************

bitmath objects come with a few basic methods: :py:meth:`to_THING`,
:py:meth:`format`, and :py:meth:`best_prefix`.


.. _instances_to_thing:

to_THING()
==========

Like the :ref:`available classes <classes_available>`, there are 24
``to_THING()`` methods available. ``THING`` is any of the bitmath
classes. You can even ``to_THING()`` an instance into itself again:


.. code-block:: python
   :linenos:
   :emphasize-lines: 3,7,12

   >>> from bitmath import *
   >>> one_mib = MiB(1)
   >>> one_mib_in_kb = one_mib.to_kb()
   >>> one_mib == one_mib_in_kb
   True

   >>> another_mib = one_mib.to_MiB()
   >>> print one_mib, one_mib_in_kb, another_mib
   1.0 MiB 8388.608 kb 1.0 MiB

   >>> six_TB = TB(6)
   >>> six_TB_in_bits = six_TB.to_Bit()
   >>> print six_TB, six_TB_in_bits
   6.0 TB 4.8e+13 Bit

   >>> six_TB == six_TB_in_bits
   True


.. _instances_best_prefix:

best_prefix()
=============

.. py:method:: best_prefix([system=None])

   Return an equivalent instance which uses the best human-readable
   prefix-unit to represent it.

   :param int system: one of :py:const:`bitmath.NIST` or :py:const:`bitmath.SI`
   :return: An equivalent :py:class:`bitmath` instance
   :rtype: :py:class:`bitmath`
   :raises ValueError: if an invalid unit system is given for ``system``


The :py:meth:`best_prefix` method returns the result of converting a
bitmath instance into an equivalent instance using a prefix unit that
better represents the original value. Another way to think of this is
automatic discovery of the most sane, or *human readable*, unit to
represent a given size. This functionality is especially important in
the domain of interactive applications which need to report file sizes
or transfer rates to users.

As an analog, consider you have 923,874,434¢ in your bank account. You
probably wouldn't want to read your bank statement and find your
balance in pennies. Most likely, your bank statement would read a
balance of $9,238,744.34. In this example, the input prefix is the
*cent*: ``¢``. The *best prefix* for this is the *dollar*: ``$``.

Let's, for example, say we are reporting a transfer rate in an
interactive application. It's important to present this information in
an easily consumable format. The library we're using to calculate the
rate of transfer reports the rate in bytes per second from a
:py:func:`tx_rate` function.

We'll use this example twice. In the first occurrence, we will print
out the transfer rate in a more easily digestible format than pure
bytes/second. In the second occurrence we'll take it a step further,
and use the :ref:`format <instances_format>` method to make the output
even easier to read.

.. code-block:: python


   >>> for _rate in tx_rate():
   ...    print "Rate: %s/second" % Bit(_rate)
   ...    time.sleep(1)

   Rate: 100.0 Bit/sec
   Rate: 24000.0 Bit/sec
   Rate: 1024.0 Bit/sec
   Rate: 60151.0 Bit/sec
   Rate: 33.0 Bit/sec
   Rate: 9999.0 Bit/sec
   Rate: 9238742.0 Bit/sec
   Rate: 2.09895849555e+13 Bit/sec
   Rate: 934098021.0 Bit/sec
   Rate: 934894.0 Bit/sec

And now using a custom formatting definition:

.. code-block:: python

   >>> for _rate in tx_rate():
   ...    print Bit(_rate).best_prefix().format("Rate: {value:.3f} {unit}/sec")
   ...    time.sleep(1)

   Rate: 12.500 Byte/sec
   Rate: 2.930 KiB/sec
   Rate: 128.000 Byte/sec
   Rate: 7.343 KiB/sec
   Rate: 4.125 Byte/sec
   Rate: 1.221 KiB/sec
   Rate: 1.101 MiB/sec
   Rate: 2.386 TiB/sec
   Rate: 111.353 MiB/sec
   Rate: 114.123 KiB/sec



.. _instances_format:

format()
========

.. py:method:: BitMathInstance.format(fmt_spec)

   Return a custom-formatted string to represent this instance.

   :param str fmt_spec: A valid formatting mini-language string
   :return: The custom formatted representation
   :rtype: ``string``


bitmath instances come with a verbose built-in string representation:

.. code-block:: python

   >>> leet_bits = Bit(1337)
   >>> print leet_bits
   1337.0 Bit

However, for instances which aren't whole numbers (as in ``MiB(1/3.0)
== 0.333333333333 MiB``, etc), their representation can be undesirable.

The :py:meth:`format` method gives you complete control over the
instance's representation. All of the :ref:`instances attributes
<instance_attributes>` are available to use when choosing a
representation.

The following sections describe some common use cases of the
:py:meth:`format` method as well as provide a :ref:`brief tutorial
<instances_mini_language>` of the greater Python formatting
meta-language.


Setting Decimal Precision
-------------------------

By default, bitmath instances will print to a fairly long precision
for values which are not whole multiples of their prefix unit. In most
use cases, simply printing out the first 2 or 3 digits of precision is
acceptable.

The following examples will show us how to print out a bitmath
instance in a more human readable way, by limiting the decimal
precision to 2 digits.

First, for reference, the default formatting:

.. code-block:: python

   >>> ugly_number = MB(50).to_MiB() / 8.0
   >>> print ugly_number
   5.96046447754 MiB

Now, let's use the :py:meth:`format` method to limit that to two
digits of precision:

.. code-block:: python

   >>> print ugly_number.format("{value:.2f}{unit}")
   5.96 MiB

By changing the **2** character, you increase or decrease the
precision. Set it to **0** (``{value:.0f}``) and you have what
effectively looks like an integer.


Format All the Instance Attributes
----------------------------------

The following example prints out every instance attribute. Take note
of how an attribute may be referenced multiple times.

.. code-block:: python
   :linenos:
   :emphasize-lines: 4,16

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

.. note:: On line **4** we print with 1 digit of precision, on line
          **16** we see the value has been rounded to **6.0**

.. _instances_properties:

Instance Properties
*******************

THING Properties
================

Like the :ref:`available classes <classes_available>`, there are 24
``THING`` properties available. ``THING`` is any of the bitmath
classes. Under the covers these properties call ``to_THING``.


.. code-block:: python
   :linenos:
   :emphasize-lines: 3,6,10

   >>> from bitmath import *
   >>> one_mib = MiB(1)
   >>> one_mib == one_mib.kb
   True

   >>> print one_mib, one_mib.kb, one_mib.MiB
   1.0 MiB 8388.608 kb 1.0 MiB

   >>> six_TB = TB(6)
   >>> print six_TB, six_TB.Bit
   6.0 TB 4.8e+13 Bit

   >>> six_TB == six_TB.Bit
   True




.. _instances_mini_language:

The Formatting Mini-Language
****************************

That is all you begin printing numbers with custom precision. If you
want to learn a little bit more about using the formatting
mini-language, read on.

You may be asking yourself where these ``{value:.2f}`` and ``{unit}``
strings came from. These are part of the `Format Specification
Mini-Language
<https://docs.python.org/3/library/string.html#format-specification-mini-language>`_
which is part of the Python standard library. To be explicitly clear
about what's going on here, let's break the first specifier
(``{value:.2f}``) down into it's component parts::

   {value:.2f}
      |  |||
      |  |||\---- The "f" says to format this as a floating point type
      |  ||\----- The 2 indicates we want 2 digits of precision (default is 6)
      |  |\------ The '.' character must precede the precision specifier for floats
      |  \------- The : separates the attribute name from the formatting specification
      \---------- The name of the attribute to print

The second specifier (``{unit}``) says to format the ``unit``
attribute as a string (string is the default type when no type is
given).

.. seealso::

   `Python String Format Cookbook <https://mkaz.blog/code/python-string-format-cookbook/>`_
      `Marcus Kazmierczak’s <https://mkaz.com/>`_ *excellent* introduction to string formatting
