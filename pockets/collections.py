# -*- coding: utf-8 -*-
# Copyright 2015 Rob Ruana
# Licensed under the BSD License, see LICENSE file for details.

"""A collection of helpful collection tools!"""

from __future__ import absolute_import
from collections import Sized, Iterable, Mapping

from pockets import six


def is_listy(x):
    """
    returns a boolean indicating whether the passed object is "listy",
    which we define as a sized iterable which is not a map or string
    """
    return (isinstance(x, Sized)
            and isinstance(x, Iterable)
            and not isinstance(x, (Mapping, type(b''), type(''))))


def listify(x, count=None):
    """
    returns a list version of x if x is a non-string iterable, otherwise
    returns a list with x as its only element
    """
    if x is None:
        x = []
    else:
        x = list(x) if is_listy(x) else [x]
    if count and len(x) < count:
        x.extend([None for i in range(count - len(x))])
    return x


def mappify(value):
    if isinstance(value, six.string_types):
        return {value: True}
    elif isinstance(value, Mapping):
        return value
    elif isinstance(value, Iterable):
        return dict([(v, True) for v in value])
    else:
        raise TypeError('Unknown datatype: {}', value)
