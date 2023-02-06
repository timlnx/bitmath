.. highlight:: python

.. _real_life_examples:

Real Life Examples
##################

.. contents::
   :depth: 3
   :local:


Download Speeds
***************

Let's pretend that your Internet service provider (ISP) advertises
your maximum downstream as **50Mbps** (50 Mega\ **bits** per second)\
:sup:`1` and you want to know how fast that is in Mega\ **bytes** per
second? ``bitmath`` can do that for you easily. We can calculate this
as such:

.. code-block:: python
   :linenos:

   >>> import bitmath
   >>> downstream = bitmath.Mib(50)
   >>> print(downstream.to_MB())
   MB(6.25)

This tells us that if our ISP advertises **50Mbps** we can expect to
see download rates of over **6MB/sec**.

1. *Assuming your ISP follows the common industry practice of using SI (base-10) units to describe file sizes/rates*


Calculating how many files fit on a device
******************************************

In 2001 Apple® announced the iPod™. Their `headline statement
<http://www.apple.com/pr/library/2001/10/23Apple-Presents-iPod.html>`_
boasting:

    "... iPod stores up to 1,000 CD-quality songs on its super-thin 5 GB hard drive, ..."

OK. That's pretty simple to work backwards: *capacity of disk drive*
divided by *number of songs* equals the average size of a song. Which
in this case is:

.. code-block:: python
   :linenos:
   :emphasize-lines: 3

   >>> song_size = GB(5) / 1000
   >>> print(song_size)
   0.005GB

Or, using ``best_prefix``, (line **2**) to generate a more
human-readable form:

.. code-block:: python
   :linenos:
   :emphasize-lines: 2

   >>> song_size = GB(5) / 1000
   >>> print(song_size.best_prefix())
   5.0MB

That's great, if you have normal radio-length songs. But how many of
our `favorite jam-band's <https://archive.org/details/moe>`_ 15-30+
minute-long songs could we fit on this iPod? Let's pretend we did the
math and the average audio file worked out to be **18.6 MiB** (19.5
MB) large.


.. code-block:: python
   :linenos:
   :emphasize-lines: 4

   >>> ipod_capacity = GB(5)
   >>> bootleg_size = MB(19.5)
   >>> print(ipod_capacity / bootleg_size)
   256.41025641

The result on line **4** tells tells us that we could fit **256**
average-quality songs on our iPod.


Printing Human-Readable File Sizes in Python
********************************************

In a Python script or interpreter we may wish to print out file sizes
in something other than bytes (which is what ``os.path.getsize``
returns). We can use ``bitmath`` to do that too:


.. code-block:: python
   :linenos:
   :emphasize-lines: 6

   >>> import os
   >>> from bitmath import *
   >>> these_files = os.listdir('.')
   >>> for f in these_files:
   ...    f_size = Byte(os.path.getsize(f))
   ...    print("%s - %s" % (f, f_size.to_KiB()))

   test_basic_math.py - 3.048828125 KiB
   __init__.py - 0.1181640625 KiB
   test_representation.py - 0.744140625 KiB
   test_to_Type_conversion.py - 2.2119140625 KiB


Alternatively, we could simplify things and use
:ref:`bitmath.getsize() <bitmath_getsize>` to read the file size
directly into a bitmath object:

.. code-block:: python
   :linenos:
   :emphasize-lines: 5

   >>> import os
   >>> import bitmath
   >>> these_files = os.listdir('.')
   >>> for f in these_files:
   ...     print("%s - %s" % (f, bitmath.getsize(f)))

   test_basic_math.py - 3.048828125 KiB
   __init__.py - 0.1181640625 KiB
   test_representation.py - 0.744140625 KiB
   test_to_Type_conversion.py - 2.2119140625 KiB


.. seealso::

   :ref:`Instance Formatting <instances_format>`
      How to print results in a *prettier* format


Calculating Linux BDP and TCP Window Scaling
********************************************

Say we're doing some Linux Kernel TCP performance tuning. For optimum
speeds we need to calculate our BDP, or Bandwidth Delay Product. For
this we need to calculate certain values to set some kernel tuning
parameters to. The point of this tuning is to send the most data we
can during a measured round-trip-time without sending more than can be
processed. To accomplish this we are resizing our kernel read/write
networking/socket buffers.

We will see two ways of doing this. The tedious manual way, and the
way with bitmath.

The Hard Way
============

**Core Networking Values**

- ``net.core.rmem_max`` - **Bytes** - Single Value - Default receive buffer size
- ``net.core.wmem_max`` - **Bytes** - Single Value - Default write buffer size

**System-Wide Memory Limits**

- ``net.ipv4.tcp_mem`` - **Pages** - Three Value Vector - The ``max``
  field of the parameter is the number of **memory pages** allowed for
  queueing by all TCP sockets.

**Per-Socket Buffers**

Per-socket buffer sizes must not exceed the core networking buffer sizes.

- ``net.ipv4.tcp_rmem`` - **Bytes** - Three Field Vector - The ``max`` field sets the size of the TCP receive buffer
- ``net.ipv4.tcp_wmem`` - **Bytes** - Three Field Vector - As above, but for the write buffer

We would normally calculate the optimal BDP and related values following this approach:

#. Measure the latency, or round trip time (RTT, measured in
   milliseconds), between the host we're tuning and our target remote
   host
#. Measure/identify our network transfer rate
#. Calculate the BDP (multiply transfer rate by rtt)
#. Obtain our current kernel settings
#. Adjust settings as necessary

But for the sake brevity we'll be working out of an example scenario
with a pre-defined RTT and transfer rate.

**Scenario**

- We have an average network transfer rate of **1Gb/sec** (where
  ``Gb`` is the SI unit for Gigabits, not Gibibytes: ``GiB``)
- Our latency (RTT) is **0.199ms** (milliseconds)

**Calculate Manually**

Lets calculate the BDP now. Because the kernel parameters expect
values in units of bytes and pages we'll have to convert our transfer
rate of 1Gb/sec into B/s (Gigabits/second to Bytes/second):

- Convert 1Gb into an equivalent **byte** based unit

Remember 1 Byte = 8 Bits:

.. code-block:: python

   tx_rate_GB = 1/8 = 0.125

Our equivalent transfer rate is 0.125GB/sec.

- Convert our RTT from milliseconds into seconds

Remember 1ms = 10\ :sup:`-3`\ s:

.. code-block:: python

   window_seconds = 0.199 * 10^-3 = 0.000199

Our equivalent RTT window is 0.000199s

- Next we multiply the transfer rate by the length of our RTT window (in seconds)

(The unit analysis for this is ``GB/s * s`` leaving us with ``GB``)

.. code-block:: python

   BDP = rx_rate_GB * window_seconds = 0.125 * 0.000199 = 0.000024875

Our BDP is 0.000024875GB.

- Convert 0.000024875GB to bytes:

Remember 1GB = 10\ :sup:`9`\ B

.. code-block:: python

   BDP_bytes = 0.000024875 * 10^9 = 24875.0

Our BDP is 24875 bytes (or about 24.3KiB)


The :py:mod:`bitmath` way
=========================


All of this math can be done much quicker (and with greater accuracy)
using the :py:mod:`bitmath` library. Let's see how:

.. code-block:: python
   :linenos:

   >>> from bitmath import GB

   >>> tx = 1/8.0

   >>> rtt = 0.199 * 10**-3

   >>> bdp = (GB(tx * rtt)).to_Byte()

   >>> print(bdp.to_KiB())

   KiB(24.2919921875)

.. note::
   To avoid integer rounding during division, don't forget to divide by ``8.0`` rather than ``8``

We could shorten that even further:

.. code-block:: python

   >>> print((GB((1/8.0) * (0.199 * 10**-3))).to_Byte())
   24875.0Byte

**Get the current kernel parameters**

Important to note is that the **per-socket** buffer sizes must not
exceed the **core network** buffer sizes. Lets fetch our current core
buffer sizes:

.. code-block:: console

   $ sysctl net.core.rmem_max net.core.wmem_max
   net.core.rmem_max = 212992
   net.core.wmem_max = 212992

Recall, these values are in bytes. What are they in KiB?

.. code-block:: python

   >>> print(Byte(212992).to_KiB())
   KiB(208.0)

This means our core networking buffer sizes are set to 208KiB
each. Now let's check our current per-socket buffer sizes:

.. code-block:: console

   $ sysctl net.ipv4.tcp_rmem net.ipv4.tcp_wmem
   net.ipv4.tcp_rmem = 4096        87380   6291456
   net.ipv4.tcp_wmem = 4096        16384   4194304

Let's double-check that our buffer sizes aren't already out of wack
(per-socket should be <= networking core)

.. code-block:: python

   >>> net_core_max = KiB(bytes=212992)

   >>> ipv4_tcp_rmem_max = KiB(bytes=6291456)

   >>> ipv4_tcp_rmem_max > net_core_max

   True

It appears that my buffers aren't sized appropriately. We'll fix that
when we set the tunable parameters.

Finally, how large is the entire system TCP buffer?

.. code-block:: console

   $ sysctl net.ipv4.tcp_mem
   net.ipv4.tcp_mem = 280632       374176  561264

Our max system TCP buffer size is set to **561264**. Recall that this
parameter is measured in **memory pages**. Most of the time your page
size is ``4096 bytes``, but you can check by running the command:
``getconf PAGESIZE``. To convert the system TCP buffer size
(561264) into a byte-based unit, we'll multiply it by our pagesize
(4096):

.. code-block:: python

   >>> sys_pages = 561264

   >>> page_size = 4096

   >>> sys_buffer = Byte(sys_pages * page_size)

   >>> print(sys_buffer.to_MiB())

   2192.4375MiB

   >>> print(sys_buffer.to_GiB())

   2.14105224609GiB

The system max TCP buffer size is about 2.14GiB.

In review, we discovered the following:

* Our **core network** buffer size is insufficient (**212992**), we'll set it higher
* Our current **per-socket** buffer sizes are **6291456** and **4194304**

And we calculated the following:

* Our ideal **max** per-socket buffer size is **24875** bytes
* Our ideal **default** per-socket buffer size (half the **max**): **12437**


**Finally: Set the new kernel parameters**

Set the **core-network** buffer sizes:

.. code-block:: console

   $ sudo sysctl net.core.rmem_max=24875  net.core.wmem_max=24875
   net.core.rmem_max = 4235
   net.core.wmem_max = 4235

Set the **per-socket** buffer sizes:

.. code-block:: console

   $ sudo sysctl net.ipv4.tcp_rmem="4096 12437 24875" net.ipv4.tcp_wmem="4096 12437 24875"
   net.ipv4.tcp_rmem = 4096 12437 24875
   net.ipv4.tcp_wmem = 4096 12437 24875

And it's done! Testing this is left as an exercise for the
reader. Note that in my experience this is less useful on wireless
connections.


.. _real_life_examples_download_progress_bars:

Creating Download Progress Bars
*******************************


.. literalinclude:: ../../full_demo.py

* View the the source for the `demo suite
  <https://raw.githubusercontent.com/tbielawa/bitmath/master/full_demo.py>`_
  on GitHub


.. _real_life_examples_read_device_storage_capacity:

Reading a Devices Storage Capacity
**********************************


.. include:: query_device_capacity_warning.rst

Using :func:`bitmath.query_device_capacity` we can read the size of a
storage device or a partition on a device.

.. include:: example_block_devices.rst

Usage is fairly straight-forward. Create an open file handle of the
device you want to read the capacity of and then create a bitmath
object with the ``query_device_capacity`` function. Here's an example
where we read the capacity of device ``sda``, the first device on the
example system.


.. code-block:: python

   >>> with open('/dev/sda', 'r') as fh:
   ...     sda_capacity = bitmath.query_device_capacity(fh)
   >>> print(sda_capacity.best_prefix())
   238.474937439 GiB
