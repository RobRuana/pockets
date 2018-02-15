# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.decorators` module."""

from __future__ import absolute_import
import pytest

from pockets.decorators import argmod, cached_classproperty, cached_property, \
    classproperty


class A(object):
    cached_classprop_count = 0

    def __init__(self):
        self.cached_prop_count = 0

    @classproperty
    def classprop(cls):
        return '{0}.classprop'.format(cls.__name__)

    @cached_classproperty
    def cached_classprop(cls):
        cls.cached_classprop_count += 1
        return '{0}.cached_classprop'.format(cls.__name__)

    @cached_property
    def cached_prop(self):
        self.cached_prop_count += 1
        return '{0}.cached_prop'.format(self.__class__.__name__)

    @cached_prop.setter
    def cached_prop(self, value):
        self._cached_cached_prop = value

    def meth(self):
        pass


def test_classproperty():
    assert A.classprop == 'A.classprop'
    assert A().classprop == 'A.classprop'

    pytest.raises(AttributeError, classproperty(A.meth).getter, A.meth)
    pytest.raises(AttributeError, classproperty(A.meth).setter, A.meth)
    pytest.raises(AttributeError, classproperty(A.meth).deleter, A.meth)


def test_cached_classproperty():
    assert A.cached_classprop_count == 0
    assert A.cached_classprop == 'A.cached_classprop'
    assert A.cached_classprop_count == 1
    assert A.cached_classprop == 'A.cached_classprop'
    assert A.cached_classprop_count == 1
    assert A().cached_classprop == 'A.cached_classprop'
    assert A.cached_classprop_count == 1
    assert A().cached_classprop == 'A.cached_classprop'
    assert A.cached_classprop_count == 1

    assert A._cached_A_cached_classprop == 'A.cached_classprop'
    del A._cached_A_cached_classprop

    assert A.cached_classprop_count == 1
    assert A.cached_classprop == 'A.cached_classprop'
    assert A.cached_classprop_count == 2
    assert A.cached_classprop == 'A.cached_classprop'
    assert A.cached_classprop_count == 2

    pytest.raises(AttributeError, cached_classproperty(A.meth).getter, A.meth)
    pytest.raises(AttributeError, cached_classproperty(A.meth).setter, A.meth)
    pytest.raises(AttributeError, cached_classproperty(A.meth).deleter, A.meth)


def test_cached_prop():
    a = A()

    assert a.cached_prop_count == 0
    assert a.cached_prop == 'A.cached_prop'
    assert a.cached_prop_count == 1
    assert a.cached_prop == 'A.cached_prop'
    assert a.cached_prop_count == 1

    assert a._cached_cached_prop == 'A.cached_prop'
    del a._cached_cached_prop

    assert a.cached_prop_count == 1
    assert a.cached_prop == 'A.cached_prop'
    assert a.cached_prop_count == 2
    assert a.cached_prop == 'A.cached_prop'
    assert a.cached_prop_count == 2

    a.cached_prop = 'UPDATED'

    assert a.cached_prop == 'UPDATED'


def echo_arg(arg):
    return arg


def echo_kwarg(kwarg='kwarg'):
    return kwarg


def reverse(arg):
    return ''.join([s for s in reversed(arg)])


class TestArgmod(object):

    def test_unknown_arg(self):
        wrapped = argmod('unknown_arg', 'unknown_arg', reverse)(echo_arg)
        assert wrapped is echo_arg
        assert wrapped('asdf') == 'asdf'

    def test_unknown_kwarg(self):
        wrapped = argmod('unknown_kwarg', 'unknown_kwarg', reverse)(echo_kwarg)
        assert wrapped is echo_kwarg
        assert wrapped('asdf') == 'asdf'

    def test_single_from_param(self):
        wrapped = argmod('arg', reverse)(echo_arg)
        assert wrapped is not echo_arg
        assert wrapped('asdf') == 'fdsa'

        wrapped = argmod('arg', 'arg', reverse)(echo_arg)
        assert wrapped is not echo_arg
        assert wrapped('asdf') == 'fdsa'

        wrapped = argmod('kwarg', reverse)(echo_kwarg)
        assert wrapped is not echo_kwarg
        assert wrapped('asdf') == 'fdsa'

        wrapped = argmod('kwarg', 'kwarg', reverse)(echo_kwarg)
        assert wrapped is not echo_kwarg
        assert wrapped('asdf') == 'fdsa'

    def test_multi_from_param(self):
        wrapped = argmod(['first_arg', 'arg'], reverse)(echo_arg)
        assert wrapped is not echo_arg
        assert wrapped('asdf') == 'fdsa'
        assert wrapped(first_arg='asdf') == 'fdsa'

        wrapped = argmod(['first_arg', 'arg'], 'arg', reverse)(echo_arg)
        assert wrapped is not echo_arg
        assert wrapped('asdf') == 'fdsa'
        assert wrapped(first_arg='asdf') == 'fdsa'

        wrapped = argmod(['first_arg', 'kwarg'], 'kwarg', reverse)(echo_kwarg)
        assert wrapped is not echo_kwarg
        assert wrapped('asdf') == 'fdsa'
        assert wrapped(first_arg='asdf') == 'fdsa'
