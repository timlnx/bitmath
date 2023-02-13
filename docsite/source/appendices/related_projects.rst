.. _appendix_related_projects:

Related Projects
****************

Bitmath is not the first project to tackle a challenge of this nature,
handling units in a sane OOP approach. Several other Python libraries
exist which provide similar functionality to bitmath. It only seems
fair that we should point out these other libraries in case bitmath
isn't the best fit for you.


Magnitude
=========

    *Magnitude implements efficient computation with physical
    quantities. It allows you to do mathematical operations with them
    as if they were numbers, taking care of the units behind the
    scenes.*


**Magnitide**, from Juan Reyero, is a *very* extensible library for
working with a large variety of units (e.g., ``mile`` = *one mile*),
as well as derived units (e.g., ``mile/hour``). Scaling, such as
indicating one **mega** byte (``1 MB``) is also programmable with
Magnitude. Juan is also kind enough to include a similar `"related
projects" <http://juanreyero.com/open/magnitude/#orgheadline12>`_
section in his documentation.

* `Magnitude GitHub Project <https://github.com/juanre/magnitude>`_
* `Magnitude Docs <http://juanreyero.com/open/magnitude/>`_



hurry.filesize
==============

    *hurry.filesize a simple Python library that can take a number of
    bytes and returns a human-readable string with the size in it, in
    kilobytes (K), megabytes (M), etc.*

**hurry.filesize** is very limited in functionality when compared to
the other alternatives. However, it is an extremely simple and
lightweight module. If you're looking for a library just for turning
counts of bytes into human-readable strings, then hurry.filesize will
be great for you.

If you need any more functionality, such as greater control over
:ref:`output formatting <module_bitmath_format>`, or :ref:`arithmetic
calculations <getting_started_arithmetic>`, then you will find
hurry.filesize lacking. This project has not updated since 2009, so I
would not expect to see updates any time soon.

* `PyPi Homepage & Download <https://pypi.python.org/pypi/hurry.filesize>`_


SymPy - Units
=============

    *This module provides around 200 predefined units that are
    commonly used in the sciences. Additionally, it provides the
    ``Unit`` class which allows you to define your own units.*

The **Units** module from the `SymPy <http://www.sympy.org/>`_ library
is another option. Like **Magnitude**, the Units library is very
extensible and includes around 200 built-in units by default. While
technically it supports handling quantities such as ``1337 PiB``, this
support must be configured by the user.

In contrast, the bitmath module includes classes representing the full
spectrum of byte and bit based units, out of the box. No conversion or
derivation code required of the user.

* `Units Homepage & Docs <https://docs.sympy.org/latest/modules/physics/units/index.html>`_
* Download available through ``pip``, or your distribution's package system
