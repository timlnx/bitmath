.. _integration_examples:

Integration Examples
####################

The following are self-contained, copy-paste examples showing how to use
:mod:`bitmath` with popular third-party libraries. These libraries are
**not** installed by bitmath — install them separately before use.

.. contents::
   :local:
   :depth: 1


.. _integration_examples_argparse:

argparse
********

The :mod:`argparse` module (part of the Python standard library) accepts
command-line arguments as strings by default.  The ``type`` parameter of
:py:meth:`~argparse.ArgumentParser.add_argument` lets you supply a
callable that converts a raw string into whatever type your application
needs.

The snippet below defines a ``BitmathType`` callable and registers it as
the type for a ``--block-size`` option so that users can write values
like ``--block-size 10MiB`` and receive a :class:`bitmath.MiB` object
directly.

.. code-block:: python

   import argparse
   import bitmath


   def BitmathType(value):
       """Convert a command-line string such as '10MiB' into a bitmath object."""
       try:
           return bitmath.parse_string(value)
       except ValueError:
           raise argparse.ArgumentTypeError(
               f"{value!r} is not a recognised bitmath unit string "
               "(examples: 10MiB, 1.5GiB, 500kB)"
           )


   def main():
       parser = argparse.ArgumentParser(
           description="Example script using a bitmath argument type"
       )
       parser.add_argument(
           "--block-size",
           type=BitmathType,
           required=True,
           help="Block size with unit, e.g. 10MiB",
       )
       args = parser.parse_args()
       print(f"Block size: {args.block_size}")
       print(f"In KiB:     {args.block_size.to_KiB():.2f}")


   if __name__ == "__main__":
       main()

Example run:

.. code-block:: bash

   $ python script.py --block-size 10MiB
   Block size: 10.0 MiB
   In KiB:     10240.00 KiB

   $ python script.py --block-size bad
   error: argument --block-size: 'bad' is not a recognised bitmath unit string (examples: 10MiB, 1.5GiB, 500kB)


.. _integration_examples_click:

click
*****

`click <https://click.palletsprojects.com/>`_ is a popular command-line
interface toolkit.  Custom parameter types are implemented by subclassing
:class:`click.ParamType` and overriding :py:meth:`~click.ParamType.convert`.

Install click before use:

.. code-block:: bash

   pip install click

.. code-block:: python

   import click
   import bitmath


   class BitmathParamType(click.ParamType):
       """A click parameter type that accepts bitmath unit strings."""

       name = "SIZE"

       def convert(self, value, param, ctx):
           if isinstance(value, bitmath.Bitmath):
               return value
           try:
               return bitmath.parse_string(value)
           except ValueError:
               self.fail(
                   f"{value!r} is not a recognised bitmath unit string "
                   "(examples: 10MiB, 1.5GiB, 500kB)",
                   param,
                   ctx,
               )


   BITMATH = BitmathParamType()


   @click.command()
   @click.option(
       "--block-size",
       type=BITMATH,
       required=True,
       help="Block size with unit, e.g. 10MiB",
   )
   def main(block_size):
       """Example command using a bitmath click parameter type."""
       click.echo(f"Block size: {block_size}")
       click.echo(f"In KiB:     {block_size.to_KiB():.2f}")


   if __name__ == "__main__":
       main()

Example run:

.. code-block:: bash

   $ python script.py --block-size 10MiB
   Block size: 10.0 MiB
   In KiB:     10240.00 KiB

   $ python script.py --block-size bad
   Error: Invalid value for '--block-size': 'bad' is not a recognised bitmath unit string (examples: 10MiB, 1.5GiB, 500kB)


.. _integration_examples_progressbar2:

progressbar2
************

`progressbar2 <https://progressbar-2.readthedocs.io/>`_ is a flexible
terminal progress-bar library.  The example below defines a custom widget
that displays a data-transfer speed (bytes per second) in a
human-readable bitmath unit, and demonstrates it with a simulated file
download.

Install progressbar2 before use:

.. code-block:: bash

   pip install progressbar2

.. code-block:: python

   import time
   import progressbar
   import bitmath


   class DataTransferSpeed(progressbar.widgets.FormatWidgetMixin,
                           progressbar.widgets.TimeSensitiveMixin):
       """Display transfer speed as a human-readable bitmath value per second."""

       def __call__(self, progress, data, **kwargs):
           elapsed = data.get("seconds_elapsed") or 0
           if elapsed <= 0 or data.get("value") is None:
               return "?? B/s"
           bytes_done = data["value"]
           speed = bitmath.Byte(bytes_done / elapsed).best_prefix()
           return f"{speed:.2f}/s"


   def simulate_download(total_bytes):
       widgets = [
           "Downloading: ",
           progressbar.Bar(),
           " ",
           progressbar.Percentage(),
           "  ",
           DataTransferSpeed(),
           " ",
           progressbar.ETA(),
       ]
       with progressbar.ProgressBar(
           max_value=total_bytes, widgets=widgets
       ) as bar:
           received = 0
           chunk = total_bytes // 50
           while received < total_bytes:
               time.sleep(0.05)
               received = min(received + chunk, total_bytes)
               bar.update(received)


   if __name__ == "__main__":
       # Simulate a 100 MiB download
       simulate_download(int(bitmath.MiB(100).to_Byte()))

Example run:

.. code-block:: text

   Downloading: |####################| 100%  18.32 MiB/s ETA:  0:00:00
