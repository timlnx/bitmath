.. _appendix_on_units:

On Units
********

As previously stated, in this module you will find two very similar
sets of classes available. These are the **NIST** and **SI**
prefixes. The **NIST** prefixes are all base 2 and have an 'i'
character in the middle. The **SI** prefixes are base 10 and have no
'i' character.

For smaller values, these two systems of unit prefixes are roughly
equivalent. The ``round()`` operations below demonstrate how close in
a percent one "unit" of SI is to one "unit" of NIST.

.. code-block:: python
   :linenos:
   :emphasize-lines: 7,15,23

   In [15]: one_kilo = 1 * 10**3

   In [16]: one_kibi = 1 * 2**10

   In [17]: round(one_kilo / one_kibi, 2)

   Out[17]: 0.98

   In [18]: one_tera = 1 * 10**12

   In [19]: one_tebi = 1 * 2**40

   In [20]: round(one_tera / one_tebi, 2)

   Out[20]: 0.91

   In [21]: one_exa = 1 * 10**18

   In [22]: one_exbi = 1 * 2**60

   In [23]: round(one_exa / one_exbi, 2)

   Out[23]: 0.87

They begin as roughly equivalent, however as you can see (lines:
**7**, **15**, and **23**), they diverge significantly for higher
values.

Why two unit systems? Why take the time to point this difference out?
Why should you care? `The Linux Documentation Project
<http://www.tldp.org/>`_ comments on that:

    Before these binary prefixes were introduced, it was fairly common
    to use k=1000 and K=1024, just like b=bit, B=byte.  Unfortunately,
    the M is capital already, and cannot be capitalized to indicate
    binary-ness.

    At first that didn't matter too much, since memory modules and
    disks came in sizes that were powers of two, so everyone knew that
    in such contexts "kilobyte" and "megabyte" meant 1024 and 1048576
    bytes, respectively.  What originally was a sloppy use of the
    prefixes "kilo" and "mega" started to become regarded as the "real
    true meaning" when computers were involved.  But then disk
    technology changed, and disk sizes became arbitrary numbers.
    After a period of uncertainty all disk manufacturers settled on
    the standard, namely k=1000, M=1000k, G=1000M.

    The situation was messy: in the 14k4 modems, k=1000; in the 1.44MB
    diskettes, M=1024000; etc.  In 1998 the IEC approved the standard
    that defines the binary prefixes given above, enabling people to
    be precise and unambiguous.

    Thus, today, MB = 1000000B and MiB = 1048576B.

    In the free software world programs are slowly being changed to
    conform.  When the Linux kernel boots and says::

        hda: 120064896 sectors (61473 MB) w/2048KiB Cache

    the MB are megabytes and the KiB are kibibytes.

- Source: ``man 7 units`` - http://man7.org/linux/man-pages/man7/units.7.html

Furthermore, to quote the `National Institute of Standards and
Technology (NIST) <http://physics.nist.gov/cuu/Units/binary.html>`_:

    "Once upon a time, computer professionals noticed that 2\ :sup:`10` was
    very nearly equal to 1000 and started using the SI prefix "kilo"
    to mean 1024. That worked well enough for a decade or two because
    everybody who talked kilobytes knew that the term implied 1024
    bytes. But, almost overnight a much more numerous "everybody"
    bought computers, and the trade computer professionals needed to
    talk to physicists and engineers and even to ordinary people, most
    of whom know that a kilometer is 1000 meters and a kilogram is
    1000 grams.

    "Then data storage for gigabytes, and even terabytes, became
    practical, and the storage devices were not constructed on binary
    trees, which meant that, for many practical purposes, binary
    arithmetic was less convenient than decimal arithmetic. The result
    is that today "everybody" does not "know" what a megabyte is. When
    discussing computer memory, most manufacturers use megabyte to
    mean 2\ :sup:`20` = 1 048 576 bytes, but the manufacturers of computer
    storage devices usually use the term to mean 1 000 000 bytes. Some
    designers of local area networks have used megabit per second to
    mean 1 048 576 bit/s, but all telecommunications engineers use it
    to mean 106 bit/s. And if two definitions of the megabyte are not
    enough, a third megabyte of 1 024 000 bytes is the megabyte used
    to format the familiar 90 mm (3 1/2 inch), "1.44 MB" diskette. The
    confusion is real, as is the potential for incompatibility in
    standards and in implemented systems.

    "Faced with this reality, the IEEE Standards Board decided that
    IEEE standards will use the conventional, internationally adopted,
    definitions of the SI prefixes. Mega will mean 1 000 000, except
    that the base-two definition may be used (if such usage is
    explicitly pointed out on a case-by-case basis) until such time
    that prefixes for binary multiples are adopted by an appropriate
    standards body."
