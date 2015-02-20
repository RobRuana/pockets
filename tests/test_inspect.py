# -*- coding: utf-8 -*-
# Copyright (c) 2015, by the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.inspect` module."""

from __future__ import absolute_import
import sys
from unittest import TestCase

import pockets
from pockets.inspect import resolve


class TestResolve(TestCase):
    def test_none(self):
        self.assertTrue(resolve(None) is None)

    def test_object(self):
        x = object()
        self.assertTrue(resolve(x) is x)
        self.assertTrue(resolve(x, "pockets") is x)
        self.assertTrue(resolve(x, ["pockets"]) is x)
        self.assertTrue(resolve(x, ["pockets", "re"]) is x)

    def test_local_module(self):
        self.assertTrue(resolve("TestResolve") is self.__class__)
        self.assertTrue(resolve("TestResolve", "tests.test_inspect") is
                        self.__class__)
        self.assertRaises(ValueError, resolve, "TestResolve", "pockets")

    def test_modules_none(self):
        self.assertTrue(resolve("pockets") is pockets)
        self.assertTrue(resolve("pockets.iterators") is pockets.iterators)
        self.assertTrue(resolve("pockets.iterators.peek_iter") is
                        pockets.iterators.peek_iter)

    def test_modules_string(self):
        dt = __import__("datetime")
        self.assertTrue(resolve("datetime") is dt)
        self.assertTrue(resolve("datetime", "datetime") is dt.datetime)
        self.assertTrue(resolve("iterators", "pockets") is pockets.iterators)
        self.assertTrue(resolve("peek_iter", "pockets.iterators") is
                        pockets.iterators.peek_iter)
        self.assertTrue(resolve("iterators.peek_iter", "pockets") is
                        pockets.iterators.peek_iter)

    def test_modules_list(self):
        dt = __import__("datetime")
        self.assertTrue(resolve("datetime") is dt)
        self.assertTrue(resolve("datetime", ["pockets", "datetime"]) is
                        dt.datetime)
        self.assertTrue(resolve("iterators", ["pockets", "datetime"]) is
                        pockets.iterators)
        self.assertTrue(resolve("iterators", ["datetime", "pockets"]) is
                        pockets.iterators)
        self.assertTrue(resolve("peek_iter",
                        ["pockets", "pockets.iterators"]) is
                        pockets.iterators.peek_iter)
        self.assertTrue(resolve("peek_iter",
                        ["pockets.iterators", "pockets"]) is
                        pockets.iterators.peek_iter)
        self.assertTrue(resolve("iterators.peek_iter",
                        ["pockets", "pockets.iterators"]) is
                        pockets.iterators.peek_iter)
        self.assertTrue(resolve("iterators.peek_iter",
                        ["pockets.iterators", "pockets"]) is
                        pockets.iterators.peek_iter)

    def test_relative_import(self):
        dt = __import__("datetime")
        self.assertTrue(resolve(".datetime") is dt)
        self.assertTrue(resolve("..datetime") is dt)
        self.assertTrue(resolve(".datetime", "datetime") is dt.datetime)
        self.assertTrue(resolve("..datetime", "datetime") is dt.datetime)
        self.assertTrue(resolve(".iterators", "pockets") is pockets.iterators)
        self.assertTrue(resolve("..iterators", "pockets") is pockets.iterators)
        self.assertTrue(resolve(".peek_iter", "pockets.iterators") is
                        pockets.iterators.peek_iter)
        self.assertTrue(resolve("..peek_iter", "pockets.iterators") is
                        pockets.iterators.peek_iter)
        self.assertTrue(resolve(".iterators.peek_iter", "pockets") is
                        pockets.iterators.peek_iter)
        self.assertTrue(resolve("..iterators.peek_iter", "pockets") is
                        pockets.iterators.peek_iter)

        mod = sys.modules["tests.test_inspect"]
        mod.MOD_ATTR = "asdf"
        self.assertEqual(resolve("MOD_ATTR"), "asdf")
        self.assertEqual(resolve(".MOD_ATTR"), "asdf")

        # Seems odd that this would raise an error, seeing as it worked
        # fine two lines above. However, resolve uses the *calling* function's
        # module as the search path, which in this case is unittest
        self.assertRaises(ValueError, resolve, "MOD_ATTR")
        self.assertRaises(ValueError, resolve, ".MOD_ATTR")

        re_mod = __import__("re")
        mod.re = "zxcv"
        self.assertTrue(resolve("re") is re_mod)
        self.assertEqual(resolve(".re"), "zxcv")
        self.assertTrue(resolve("..re") is re_mod)
        self.assertTrue(resolve("...re") is re_mod)
        self.assertEqual(resolve("re", "tests.test_inspect"), "zxcv")
        self.assertEqual(resolve(".re", "tests.test_inspect"), "zxcv")
        self.assertEqual(resolve("..re", "tests.test_inspect"), "zxcv")
        self.assertEqual(resolve("test_inspect.re", "tests"), "zxcv")
        self.assertEqual(resolve(".test_inspect.re", "tests"), "zxcv")
        self.assertEqual(resolve("..test_inspect.re", "tests"), "zxcv")

    def test_raises(self):
        self.assertRaises(ValueError, resolve, "NOTFOUND")
        self.assertRaises(ValueError, resolve, "pockets.NOTFOUND")
        self.assertRaises(ValueError, resolve, "NOTFOUND", "pockets")
        self.assertRaises(ValueError, resolve, "NOTFOUND", ["pockets"])
        self.assertRaises(ValueError, resolve, "NOTFOUND", ["pockets", "re"])
