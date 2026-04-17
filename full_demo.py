#!/usr/bin/env python
# SPDX-License-Identifier: MIT
from __future__ import print_function
import logging
import time
import bitmath
from bitmath.integrations.bmargparse import BitmathType
from bitmath.integrations.bmprogressbar import BitmathFileTransferSpeed
import argparse
import requests
import progressbar
import os
import tempfile
import atexit
import random
from functools import reduce

# Files of various sizes to use in the demo.
#
# Moar here: https://www.kernel.org/pub/linux/kernel/v3.0/?C=S;O=D
REMOTES = [
    # patch-3.0.70.gz         20-Mar-2013 20:02  1.0M
    'https://www.kernel.org/pub/linux/kernel/v3.0/patch-3.4.92.xz',

    # patch-3.16.gz           03-Aug-2014 22:39  8.0M
    'https://www.kernel.org/pub/linux/kernel/v3.0/patch-3.16.gz',

    # patch-3.2.gz            05-Jan-2012 00:43   22M
    'https://www.kernel.org/pub/linux/kernel/v3.0/patch-3.2.gz',
]

######################################################################
p = argparse.ArgumentParser(description='bitmath demo suite')
p.add_argument('-d', '--down', help="Download Rate",
               type=BitmathType,
               default=bitmath.MiB(4))

p.add_argument('-s', '--slowdown',
               help='Randomly pause to slow down the transfer rate',
               action='store_true', default=False)

args = p.parse_args()

######################################################################
# Save our example files somewhere. And then clean up every trace that
# anything every happened there. shhhhhhhhhhhhhhhh
DESTDIR = tempfile.mkdtemp('demosuite', 'bitmath')
@atexit.register
def cleanup():
    for f in os.listdir(DESTDIR):
        os.remove(os.path.join(DESTDIR, f))
    os.rmdir(DESTDIR)

######################################################################
for f in REMOTES:
    print("""
######################################################################""")
    fname = os.path.basename(f)
    # An array of widgets to design our progress bar. Note how we use
    # BitmathFileTransferSpeed
    widgets = ['Bitmath Demo Suite (%s): ' % fname,
               progressbar.Percentage(), ' ',
               progressbar.Bar(marker=progressbar.RotatingMarker()), ' ',
               progressbar.ETA(), ' ',
               BitmathFileTransferSpeed()]

    # The 'stream' keyword lets us http GET files in
    # chunks. http://docs.python-requests.org/en/latest/user/quickstart/#raw-response-content
    r = requests.get(f, stream=True)
    # We haven't began receiving the payload content yet, we have only
    # just received the response headers. Of interest is the
    # 'content-length' header which describes our payload in bytes
    #
    # http://bitmath.readthedocs.org/en/latest/classes.html#bitmath.Byte
    size = bitmath.Byte(int(r.headers['Content-Length']))

    # Demonstrate 'with' context handler, allowing us to customize all
    # bitmath string printing within the indented block. We don't need
    # all that precision anyway, just two points should do.
    #
    # http://bitmath.readthedocs.org/en/latest/module.html#bitmath-format
    with bitmath.format("{value:.2f} {unit}"):
        print("Downloading %s (%s) in %s chunks" % (f,
                                                    size.best_prefix(),
                                                    args.down.best_prefix()))

    # We have to save these files somewhere
    save_path = os.path.join(DESTDIR, fname)
    print("Saving to: %s" % save_path)
    print("")

    # OK. Let's create our actual progress bar now. See the 'maxval'
    # keyword? That's the size of our payload in bytes.
    pbar = progressbar.ProgressBar(
        widgets=widgets,
        maxval=int(size)).start()

    ######################################################################
    # Open a new file for binary writing and write 'args.down' size
    # chunks into it until we've received the entire payload
    with open(save_path, 'wb') as fd:
        # The 'iter_content' method accepts integer values of
        # bytes. Lucky for us, 'args.down' is a bitmath instance and
        # has a 'bytes' attribute we can feed into the method call.
        for chunk in r.iter_content(int(args.down.bytes)):
            fd.write(chunk)
            # The progressbar will end the entire cosmos as we know it
            # if we try to .update() it beyond it's MAXVAL
            # parameter.
            #
            # That's something I'd like to avoid taking the
            # responsibility for.
            if (pbar.currval + args.down.bytes) < pbar.maxval:
                pbar.update(pbar.currval + int(args.down.bytes))

            # We can add an pause to artificially speed up/slowdown
            # the transfer rate. Allows us to see different units.
            if args.slowdown:
                # randomly slow down 1/5 of the time
                if random.randrange(0, 100) % 5 == 0:
                    time.sleep(random.randrange(0, 500) * 0.01)

    # Nothing to see here. Go home.
    pbar.finish()

######################################################################
print("""
######################################################################
List downloaded contents
* Filter for .xz files only
""")

for p,bm in bitmath.listdir(DESTDIR,
                            filter='*.xz'):
    print(p, bm)

######################################################################
print("""
######################################################################
List downloaded contents
* Filter for .gz files only
* Print using best human readable prefix
""")

for p,bm in bitmath.listdir(DESTDIR,
                            filter='*.gz',
                            bestprefix=True):
    print(p, bm)

######################################################################
print("""
######################################################################
List downloaded contents
* No filter set, to display all files
* Limit precision of printed file size to 3 digits
* Print using best human readable prefix
""")

for p,bm in bitmath.listdir(DESTDIR,
                            bestprefix=True):
    with bitmath.format("{value:.3f} {unit}"):
        print(p, bm)

######################################################################
print("""
######################################################################
Sum the size of all downloaded files together
* Print with best prefix and 3 digits of precision
""")

discovered_files = [f[1] for f in bitmath.listdir(DESTDIR)]
total_size = reduce(lambda x,y: x+y, discovered_files).best_prefix().format("{value:.3f} {unit}")
print("Total size of %s downloaded items: %s" % (len(discovered_files), total_size))
