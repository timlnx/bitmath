.. _appendix_math:

Rules for Math
**************

This section describes what we need to know to effectively use bitmath
for arithmetic. Because bitmath allows the use of instances as
operands on either side of the operator it is especially important to
understand their behavior. Just as in normal every-day math, not all
operations yield the same result if the operands are switched. E.g.,
``1 - 2 = -1`` whereas ``2 - 1 = 1``.

This section includes discussions of the results for each supported
**mixed math** operation. For mixed math operations (i.e., an
operation with a bitmath instance and a number type), implicit
coercion **may** happen. That is to say, a bitmath instance will be
converted to a number type.

When coercion happens is determined by the following conditions and
rules:

1. `Precedence and Associativity of Operators
   <https://docs.python.org/3/reference/expressions.html#operator-precedence>`_
   in Python\ [#precedence]_
2. Situational semantics -- some operations, though mathematically
   valid, do not make logical sense when applied to context.


Terminology
===========

The definitions describes some of the terminology used throughout this
section.

Coercion
   The act of converting operands into a common type to support
   arithmetic operations. Somewhat similar to how adding two fractions
   requires coercing each operand into having a common denominator.

   Specific to the bitmath domain, this concept means using an
   instance's prefix value for mixed-math.

Operand
   The object(s) of a mathematical operation. That is to say, given
   ``1 + 2``, the operands would be **1** and **2**.

Operator
   The mathematical operation to evaluate. Given ``1 + 2``, the
   operation would be addition, **+**.

LHS
   *Left-hand side*. In discussion this specifically refers to the
   operand on the left-hand side of the operator.

RHS
   *Right-hand side*. In discussion this specifically refers to the
   operand on the right-hand side of the operator.



Two bitmath operands
====================

This section describes what happens when two bitmath instances are
used as operands. There are three possible results from this type of
operation.

*Addition and subtraction*
  The result will be of the type of the LHS.

*Multiplication*
   Supported, but yields strange results.

.. code-block:: python
   :linenos:
   :emphasize-lines: 6,9

   In [10]: first = MiB(5)

   In [11]: second = kB(2)

   In [12]: first * second
   Out[12]: MiB(10000.0)

   In [13]: (first * second).best_prefix()
   Out[13]: GiB(9.765625)

As we can see on lines **6** and **9**, multiplying even two
relatively small quantities together (``MiB(5)`` and ``kB(2)``) yields
quite large results.

Internally, this is implemented as:

.. math::

   (5 \cdot 2^{20}) \cdot (2 \cdot 10^{3}) = 10,485,760,000 B

   10,485,760,000 B \cdot \dfrac{1 MiB}{1,048,576 B} = 10,000 MiB

*Division*
   The result will be a number type due to unit cancellation.


Mixed Types: Addition and Subtraction
=====================================

This describes the behavior of addition and subtraction operations
where one operand is a bitmath type and the other is a number type.

Mixed-math addition and subtraction **always** return a type from the
:py:mod:`numbers` family (integer, float, long, etc...). This rule is
true regardless of the placement of the operands, with respect to the
operator.

**Discussion:** Why do ``100 - KiB(90)`` and ``KiB(100) - 90`` both
yield a result of ``10.0`` and not another bitmath instance, such as
``KiB(10.0)``?

When implementing the math part of the object datamodel
customizations\ [#datamodel]_ there were two choices available:

1. Offer no support at all. Instead raise a :py:exc:`NotImplemented`
   exception.

2. Consistently apply coercion to the bitmath operand to produce a
   useful result (*useful* if you know the rules of the library).

In the end it became a philosophical decision guided by scientific
precedence.

Put simply, bitmath uses the significance of the **least significant
operand**, specifically the number-type operand because it lacks
semantic significance. In application this means that we drop the
semantic significance of the bitmath operand. That is to say, given an
input like ``GiB(13.37)`` (equivalent to == 13.37 * 2\ :sup:`30`\ ), the
only property used in calculations is the prefix value, ``13.37``.

Numbers carry mathematical significance, in the form of precision, but
what they lack is *semantic* (contextual) significance. A number by
itself is just a measurement of an arbitrary quantity of *stuff*. In
mixed-type math, bitmath effectively treats numbers as mathematical
constants.

A bitmath instance also has mathematical significance in that an
instance is a measurement of a quantity (bits in this case) and that
quantity has a measurable precision. But a bitmath instance is more
than just a measurement, it is a specialized representation of a count
of bits. This gives bitmath instances *semantic* significance as well.

And so, in deciding how to handle mixed-type (really what we should
say is mixed-significance) operations, we chose to model the behavior
off of an already established set of rules. Those rules are the Rules
of Significance Arithmetic\ [#significance]_.

Let's look at an example of this in action:

.. code-block:: python

   In [8]: num = 42

   In [9]: bm = PiB(24)

   In [10]: print(num + bm)
   66.0

Equivalently, divorcing the bitmath instance from it's value (this is
coercion):

.. code-block:: python

   In [12]: bm_value = bm.value

   In [13]: print(num + bm_value)
   66.0

What it all boils down to is this: if we don't provide a unit then
bitmath won't give us one back. There is no way for bitmath to guess
what unit the operand was *intended* to carry. Therefore, the behavior
of bitmath is **conservative**. It will meet us half way and do the
math, but it will not return a unit in the result.


Mixed Types: Multiplication and Division
========================================

**Multiplication** has *commutative* properties. This means that the
ordering of the operands is **not significant**. Because of this fact
bitmath allows arbitrary placement of the operands, treating the
numeric operand as a constant. Here's an example demonstrating this.

.. code-block:: python

   In [2]: 10 * KiB(43)
   Out[2]: KiB(430.0)

   In [3]: KiB(43) * 10
   Out[3]: KiB(430.0)


**Division**, however, *does not* have this commutative
property. I.e., the placement of the operands **is**
significant. Additionally, there is a semantic difference in
division. Dividing a quantity (e.g. ``MiB(100)``) by a constant
(``10``) makes complete sense. Conceptually (in the domain of
bitmath), the intention of ``MiB(100) / 10)`` is to separate
``MiB(10)`` into **10** equal sized parts.

.. code-block:: python

   In [4]: KiB(43) / 10
   Out[4]: KiB(4.2998046875)

The reverse operation does not maintain semantic validity. Stated
differently, it does not make logical sense to divide a constant by a
measured quantity of *stuff*. If you're still not clear on this, ask
yourself what you would expect to get if you did this:

.. math::

   \dfrac{100}{kB(33)} = x



Footnotes
=========

.. [#precedence] For a less technical review of precedence and associativity,
       see `Programiz: Precedence and Associativity of Operators in
       Python
       <https://www.programiz.com/python-programming/precedence-associativity>`_

.. [#datamodel] `Python Datamodel Customization Methods
                <https://docs.python.org/2.7/reference/datamodel.html#basic-customization>`_

.. [#significance] https://en.wikipedia.org/wiki/Significance_arithmetic
