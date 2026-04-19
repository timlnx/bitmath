.. _command_line:

The ``bitmath`` command-line Tool
#################################

:mod:`bitmath` includes a CLI utility for easily converting units in a
shell. For reference, there is also a manpage included,
:manpage:`bitmath (1)`.

Synopsis
********

.. code-block:: bash

   bitmath [--from-stdin] [-f IN_UNIT] [-t OUT_UNIT] VALUE ...


Options
*******

.. program:: bitmath

.. option:: -f <IN_UNIT>

   Specify the input unit to convert from. Defaults to
   :class:`bitmath.Byte`.


.. option:: -t <OUT_UNIT>

   Specify the output unit to convert to. Defaults to the :ref:`best
   human-readable <instances_best_prefix>` prefix unit.

.. option:: --from-stdin

   Reads number from stdin rather than as a CLI argument.

.. describe:: VALUE

   The value to convert.


Examples
********

Convert ``1024`` into the best human-readable unit. Without specifying
any ``from`` or ``to`` values this examples defaults to treating the
input value as a :class:`bitmath.Byte`:

.. code-block:: bash

   $ bitmath 1024
   1.00 KiB

Convert 1024 KiB into kBs:

.. code-block:: bash

   $ bitmath -f KiB -t kb 1024
   8388.608 kb

Convert 1073741824 bytes into the best human-readable unit:

.. code-block:: bash

   $ bitmath -f Byte 1073741824
   1.00 GiB

Use the :command:`stat` command to print the size of
:file:`bitmath/__init__.py` in bytes, pipe the output into the
:command:`bitmath` command, and print the result in MBs:

.. code-block:: bash

   $ stat -c '%s' bitmath/__init__.py | bitmath --from-stdin -t MB
   0.038374 MB

Convert several values at once from Bytes (the default behavior) into MBs:

.. code-block:: bash

   $ bitmath -t MB 1234567 9876543 1337 42
   1.234567 MB
   9.876543 MB
   0.001337 MB
   4.2e-05 MB
