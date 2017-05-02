# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.decorators` module."""

from __future__ import absolute_import
import pytest
from pockets.decorators import classproperty


class A(object):
    @classproperty
    def prop(cls):
        return '{0}.prop'.format(cls.__name__)

    def meth(cls):
        pass


def test_classproperty():
    assert A.prop == 'A.prop'
    assert A().prop == 'A.prop'
    pytest.raises(AttributeError, classproperty(A.meth).getter, A.meth)
    pytest.raises(AttributeError, classproperty(A.meth).setter, A.meth)
    pytest.raises(AttributeError, classproperty(A.meth).deleter, A.meth)
