.. _classes:

.. currentmodule:: bitmath

Classes
#######

.. contents::
   :depth: 3
   :local:

Available Classes
*****************

There are two **fundamental** classes available, the :class:`Bit` and
the :class:`Byte`.

There are **24** other classes available, representing all the prefix
units from **k** through **e** (*kilo/kibi* through *exa/exbi*).

Classes with **'i'** in their names are **NIST** type classes. They
were defined by the `National Institute of Standards and Technology
(NIST) <https://www.nist.gov/>`_ as the 'Binary Prefix Units'. They are
defined by increasing powers of 2.

Classes without the **'i'** character are **SI** type classes. Though
not formally defined by any standards organization, they follow the
`International System of Units (SI)
<http://www.bipm.org/en/publications/si-brochure/chapter3.html>`_
pattern (commonly used to abbreviate base 10 values). You may hear
these referred to as the "Decimal" or "SI" prefixes.

Classes ending with *lower-case* **'b'** characters are **bit
based**. Classes ending with upper-case **'B'** characters are **byte
based**. Class inheritance is shown below in parentheses to make this
more apparent:

.. _classes_available:

+---------------+--------------+
| NIST          | SI           |
+===============+==============+
| ``Eib(Bit)``  | ``Eb(Bit)``  |
+---------------+--------------+
| ``EiB(Byte)`` | ``EB(Byte)`` |
+---------------+--------------+
| ``Gib(Bit)``  | ``Gb(Bit)``  |
+---------------+--------------+
| ``GiB(Byte)`` | ``GB(Byte)`` |
+---------------+--------------+
| ``Kib(Bit)``  | ``kb(Bit)``  |
+---------------+--------------+
| ``KiB(Byte)`` | ``kB(Byte)`` |
+---------------+--------------+
| ``Mib(Bit)``  | ``Mb(Bit)``  |
+---------------+--------------+
| ``MiB(Byte)`` | ``MB(Byte)`` |
+---------------+--------------+
| ``Pib(Bit)``  | ``Pb(Bit)``  |
+---------------+--------------+
| ``PiB(Byte)`` | ``PB(Byte)`` |
+---------------+--------------+
| ``Tib(Bit)``  | ``Tb(Bit)``  |
+---------------+--------------+
| ``TiB(Byte)`` | ``TB(Byte)`` |
+---------------+--------------+

.. note:: As per SI definition, the ``kB`` and ``kb`` classes begins
          with a *lower-case* **k** character.

The majority of the functionality of bitmath object comes from their
rich implementation of standard Python operations. You can use bitmath
objects in **almost all** of the places you would normally use an
integer or a float. See the :ref:`Table of Supported Operations
<simple_examples_supported_operations>` and :ref:`Appendix: Rules for
Math <appendix_math>` for more details.


Initializing
************

.. class:: Bit([value=0[, bytes=None[, bits=None]]])
.. class:: Byte([value=0[, bytes=None[, bits=None]]])
.. class:: EB([value=0[, bytes=None[, bits=None]]])
.. class:: Eb([value=0[, bytes=None[, bits=None]]])
.. class:: EiB([value=0[, bytes=None[, bits=None]]])
.. class:: Eib([value=0[, bytes=None[, bits=None]]])
.. class:: GB([value=0[, bytes=None[, bits=None]]])
.. class:: Gb([value=0[, bytes=None[, bits=None]]])
.. class:: GiB([value=0[, bytes=None[, bits=None]]])
.. class:: Gib([value=0[, bytes=None[, bits=None]]])
.. class:: kB([value=0[, bytes=None[, bits=None]]])
.. class:: kb([value=0[, bytes=None[, bits=None]]])
.. class:: KiB([value=0[, bytes=None[, bits=None]]])
.. class:: Kib([value=0[, bytes=None[, bits=None]]])
.. class:: MB([value=0[, bytes=None[, bits=None]]])
.. class:: Mb([value=0[, bytes=None[, bits=None]]])
.. class:: MiB([value=0[, bytes=None[, bits=None]]])
.. class:: Mib([value=0[, bytes=None[, bits=None]]])
.. class:: PB([value=0[, bytes=None[, bits=None]]])
.. class:: Pb([value=0[, bytes=None[, bits=None]]])
.. class:: PiB([value=0[, bytes=None[, bits=None]]])
.. class:: Pib([value=0[, bytes=None[, bits=None]]])
.. class:: TB([value=0[, bytes=None[, bits=None]]])
.. class:: Tb([value=0[, bytes=None[, bits=None]]])
.. class:: TiB([value=0[, bytes=None[, bits=None]]])
.. class:: Tib([value=0[, bytes=None[, bits=None]]])
.. class:: YB([value=0[, bytes=None[, bits=None]]])
.. class:: Yb([value=0[, bytes=None[, bits=None]]])
.. class:: ZB([value=0[, bytes=None[, bits=None]]])
.. class:: Zb([value=0[, bytes=None[, bits=None]]])

.. class:: Bitmath([value=0[, bytes=None[, bits=None]]])

   The ``value``, ``bytes``, and ``bits`` parameters are **mutually
   exclusive**. That is to say, you cannot instantiate a bitmath class
   using more than **one** of the parameters. Omitting any keyword
   argument defaults to behaving as if ``value`` was provided.

   :param int value: **Default: 0**. The value of the instance in
                     *prefix units*. For example, if we were
                     instantiating a ``bitmath.KiB`` object to
                     represent 13.37 KiB, the ``value`` parameter
                     would be **13.37**. For instance, ``k =
                     bitmath.KiB(13.37)``.
   :param int bytes: The value of the instance as measured in bytes.
   :param int bits: The value of the instance as measured in bits.
   :raises ValueError: if more than one parameter is provided.

The following code block demonstrates the 4 acceptable ways to
instantiate a bitmath class.


.. code-block:: python
   :linenos:
   :emphasize-lines: 4,7,11,15

   >>> import bitmath

   # Omitting all keyword arguments defaults to 'value' behavior.
   >>> a = bitmath.KiB(1)

   # This is equivalent to the previous statement
   >>> b = bitmath.KiB(value=1)

   # We can also specify the initial value in bytes.
   # Recall, 1KiB = 1024 bytes
   >>> c = bitmath.KiB(bytes=1024)

   # Finally, we can specify exact number of bits in the
   # instance. Recall, 1024B = 8192b
   >>> d = bitmath.KiB(bits=8192)

   >>> a == b == c == d
   True


Class Methods
*************


Class Method: from_other()
==========================

bitmath **class objects** have one public class method,
:py:meth:`BitMathClass.from_other` which provides an
alternative way to initialize a bitmath class.

This method may be called on bitmath class objects directly. That is
to say: you do not need to call this method on an instance of a
bitmath class, however that is a valid use case.


.. classmethod:: Byte.from_other(item)

   Instantiate any ``BitMathClass`` using another instance as
   reference for it's initial value.

   The ``from_other()`` class method has one required parameter: an
   instance of a bitmath class.

   :param BitMathInstance item: An instance of a bitmath class.
   :return: a bitmath instance of type ``BitMathClass`` equivalent in
            value to ``item``
   :rtype: BitMathClass
   :raises TypeError: if ``item`` is not a valid :ref:`bitmath class
                      <classes_available>`

   In pure Python, this could also be written as:

   .. code-block:: python
      :linenos:
      :emphasize-lines: 3

      >>> import bitmath

      >>> a_mebibyte = bitmath.MiB(1)

      >>> a_mebibyte_sized_kibibyte = bitmath.KiB(bytes=a_mebibyte.bytes)

      >>> a_mebibyte == a_mebibyte_sized_kibibyte
      True

      >>> print(a_mebibyte, a_mebibyte_sized_kibibyte)
      1.0 MiB 1024.0 KiB

   Or, using the :py:meth:`BitMathClass.from_other` class method:

   .. code-block:: python
      :linenos:

      >>> a_mebibyte = bitmath.MiB(1)

      >>> a_big_kibibyte = bitmath.KiB.from_other(a_mebibyte)

      >>> a_mebibyte == a_big_kibibyte
      True

      >>> print(a_mebibyte, a_big_kibibyte)
      1.0 MiB 1024.0 KiB
