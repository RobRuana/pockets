# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.inspect` module."""

from __future__ import absolute_import
import sys

import pockets
import pytest
from pockets.inspect import resolve


class TestResolve(object):
    def test_none(self):
        assert resolve(None) is None

    def test_object(self):
        x = object()
        assert resolve(x) is x
        assert resolve(x, 'pockets') is x
        assert resolve(x, ['pockets']) is x
        assert resolve(x, ['pockets', 're']) is x

    def test_local_module(self):
        assert resolve('TestResolve') is self.__class__
        assert resolve('TestResolve', 'tests.test_inspect') is self.__class__
        pytest.raises(ValueError, resolve, 'TestResolve', 'pockets')

    def test_modules_none(self):
        assert resolve('pockets') is pockets
        assert resolve('pockets.iterators') is pockets.iterators
        assert resolve('pockets.iterators.peek_iter') is \
            pockets.iterators.peek_iter

    def test_modules_string(self):
        dt = __import__('datetime')
        assert resolve('datetime') is dt
        assert resolve('datetime', 'datetime') is dt.datetime
        assert resolve('iterators', 'pockets') is pockets.iterators
        assert resolve('peek_iter', 'pockets.iterators') is \
            pockets.iterators.peek_iter
        assert resolve('iterators.peek_iter', 'pockets') is \
            pockets.iterators.peek_iter

    def test_modules_list(self):
        dt = __import__('datetime')
        assert resolve('datetime') is dt
        assert resolve('datetime', ['pockets', 'datetime']) is dt.datetime
        assert resolve('iterators', ['pockets', 'datetime']) is \
            pockets.iterators
        assert resolve('iterators', ['datetime', 'pockets']) is \
            pockets.iterators
        assert resolve('peek_iter', ['pockets', 'pockets.iterators']) is \
            pockets.iterators.peek_iter
        assert resolve('peek_iter', ['pockets.iterators', 'pockets']) is \
            pockets.iterators.peek_iter
        assert resolve(
            'iterators.peek_iter', ['pockets', 'pockets.iterators']) is \
            pockets.iterators.peek_iter
        assert resolve(
            'iterators.peek_iter', ['pockets.iterators', 'pockets']) is \
            pockets.iterators.peek_iter

    def test_relative_import(self):
        dt = __import__('datetime')
        assert resolve('.datetime') is dt
        assert resolve('..datetime') is dt
        assert resolve('.datetime', 'datetime') is dt.datetime
        assert resolve('..datetime', 'datetime') is dt.datetime
        assert resolve('.iterators', 'pockets') is pockets.iterators
        assert resolve('..iterators', 'pockets') is pockets.iterators
        assert resolve('.peek_iter', 'pockets.iterators') is \
            pockets.iterators.peek_iter
        assert resolve('..peek_iter', 'pockets.iterators') is \
            pockets.iterators.peek_iter
        assert resolve('.iterators.peek_iter', 'pockets') is \
            pockets.iterators.peek_iter
        assert resolve('..iterators.peek_iter', 'pockets') is \
            pockets.iterators.peek_iter

        mod = sys.modules['tests.test_inspect']
        mod.MOD_ATTR = 'asdf'
        assert resolve('MOD_ATTR') == 'asdf'
        assert resolve('.MOD_ATTR') == 'asdf'

        # Seems odd that this would raise an error, seeing as it worked
        # fine two lines above. However, resolve uses the *calling* function's
        # module as the search path, which in this case is unittest
        pytest.raises(ValueError, resolve, 'MOD_ATTR')
        pytest.raises(ValueError, resolve, '.MOD_ATTR')

        re_mod = __import__('re')
        mod.re = 'zxcv'
        assert resolve('re') is re_mod
        assert resolve('.re') == 'zxcv'
        assert resolve('..re') is re_mod
        assert resolve('...re') is re_mod
        assert resolve('re', 'tests.test_inspect') == 'zxcv'
        assert resolve('.re', 'tests.test_inspect') == 'zxcv'
        assert resolve('..re', 'tests.test_inspect') == 'zxcv'
        assert resolve('test_inspect.re', 'tests') == 'zxcv'
        assert resolve('.test_inspect.re', 'tests') == 'zxcv'
        assert resolve('..test_inspect.re', 'tests') == 'zxcv'

    def test_raises(self):
        pytest.raises(ValueError, resolve, 'NOTFOUND')
        pytest.raises(ValueError, resolve, 'pockets.NOTFOUND')
        pytest.raises(ValueError, resolve, 'NOTFOUND', 'pockets')
        pytest.raises(ValueError, resolve, 'NOTFOUND', ['pockets'])
        pytest.raises(ValueError, resolve, 'NOTFOUND', ['pockets', 're'])
