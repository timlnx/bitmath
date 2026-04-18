# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# The MIT License (MIT)
#
# Copyright © 2026 Tim Case <bitmath@lnx.cx>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Thread-safety tests for the bitmath.format() context manager.

These tests verify that concurrent context managers in different threads
are fully isolated: one thread's format_string, plural, and bestprefix
settings cannot bleed into another thread's context.

Regression coverage for GitHub issue #83.
"""

import queue
import threading

from . import TestCase
import bitmath


THREAD_COUNT = 8


class TestContextManagerThreadSafety(TestCase):

    def test_format_string_isolation(self):
        """Concurrent format contexts expose only their own format_string (issue #83)

Each of THREAD_COUNT threads enters a context with a unique format string,
then all wait at a barrier so they are guaranteed to be inside their
respective contexts simultaneously before formatting any strings.
        """
        errors = queue.Queue()
        barrier = threading.Barrier(THREAD_COUNT)

        def worker(thread_id):
            fmt = "{value}-T" + str(thread_id)
            expected = "1.0-T" + str(thread_id)
            try:
                with bitmath.format(fmt_str=fmt):
                    barrier.wait()
                    result = str(bitmath.KiB(1))
                    if result != expected:
                        errors.put(AssertionError(
                            "Thread %d: expected %r, got %r" % (
                                thread_id, expected, result)))
            except Exception as exc:
                errors.put(exc)

        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(THREAD_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if not errors.empty():
            raise errors.get()

    def test_plural_isolation(self):
        """Concurrent format contexts expose only their own plural setting"""
        errors = queue.Queue()
        barrier = threading.Barrier(THREAD_COUNT)

        def plural_worker(expect_plural):
            try:
                with bitmath.format(plural=expect_plural):
                    barrier.wait()
                    result = str(bitmath.Byte(3.0))
                    if expect_plural and result != "3.0 Bytes":
                        errors.put(AssertionError(
                            "plural thread: expected '3.0 Bytes', got %r" % result))
                    elif not expect_plural and result != "3.0 Byte":
                        errors.put(AssertionError(
                            "singular thread: expected '3.0 Byte', got %r" % result))
            except Exception as exc:
                errors.put(exc)

        threads = [
            threading.Thread(target=plural_worker, args=(i % 2 == 0,))
            for i in range(THREAD_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if not errors.empty():
            raise errors.get()

    def test_bestprefix_isolation(self):
        """Concurrent format contexts expose only their own bestprefix setting"""
        errors = queue.Queue()
        barrier = threading.Barrier(THREAD_COUNT)

        def bestprefix_worker(use_bestprefix):
            try:
                with bitmath.format(bestprefix=use_bestprefix):
                    barrier.wait()
                    result = str(bitmath.MiB(1024))
                    if use_bestprefix and result != "1.0 GiB":
                        errors.put(AssertionError(
                            "bestprefix thread: expected '1.0 GiB', got %r" % result))
                    elif not use_bestprefix and result != "1024.0 MiB":
                        errors.put(AssertionError(
                            "no-bestprefix thread: expected '1024.0 MiB', got %r" % result))
            except Exception as exc:
                errors.put(exc)

        threads = [
            threading.Thread(target=bestprefix_worker, args=(i % 2 == 0,))
            for i in range(THREAD_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if not errors.empty():
            raise errors.get()

    def test_issue_83_format_string_race(self):
        """Reproduces the exact race condition reported in GitHub issue #83

The module-level format_string is set to an invalid key. Each thread
enters a context that supplies a valid format string. Without thread-
local storage all threads would see the invalid format_string after any
one of them exits its context, producing a KeyError.
        """
        saved = bitmath.format_string
        bitmath.format_string = "{not_a_valid_key}"
        errors = queue.Queue()
        barrier = threading.Barrier(THREAD_COUNT)

        def worker():
            try:
                with bitmath.format(fmt_str=saved):
                    barrier.wait()
                    str(bitmath.KiB(1))
            except Exception as exc:
                errors.put(exc)

        threads = [threading.Thread(target=worker) for _ in range(THREAD_COUNT)]
        try:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        finally:
            bitmath.format_string = saved

        if not errors.empty():
            raise errors.get()

    def test_module_global_unchanged_by_context(self):
        """The module-level format_string is never mutated by the context manager"""
        original = bitmath.format_string
        with bitmath.format(fmt_str="{value:.4f} {unit}"):
            self.assertEqual(bitmath.format_string, original)
        self.assertEqual(bitmath.format_string, original)

    def test_format_string_restored_after_exception_in_thread(self):
        """Thread-local state is cleaned up even when an exception escapes the with block"""
        errors = queue.Queue()

        def worker():
            try:
                try:
                    with bitmath.format(fmt_str="{value:.2f} {unit}"):
                        raise ValueError("intentional")
                except ValueError:
                    pass
                result = str(bitmath.KiB(1))
                if result != "1.0 KiB":
                    errors.put(AssertionError(
                        "after exception: expected '1.0 KiB', got %r" % result))
            except Exception as exc:
                errors.put(exc)

        t = threading.Thread(target=worker)
        t.start()
        t.join()

        if not errors.empty():
            raise errors.get()
