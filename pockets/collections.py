# -*- coding: utf-8 -*-
# Copyright 2015 Rob Ruana
# Licensed under the BSD License, see LICENSE file for details.

"""A collection of helpful collection tools!"""

from __future__ import absolute_import
from collections import Sized, Iterable, Mapping

import six

__all__ = ["is_listy", "listify", "mappify"]


def is_listy(x):
    """Return True if the object is "listy", i.e. a list-like object.

    "Listy" is defined as a sized iterable which is neither a map or string:
        >>> is_listy(["a", "b"])
        True
        >>> is_listy(set())
        True
        >>> is_listy({"a": "b"})
        False
        >>> is_listy("Just a string")
        False

    """
    return (isinstance(x, Sized) and
            isinstance(x, Iterable) and
            not isinstance(x, Mapping) and
            not isinstance(x, six.string_types))


def listify(x, minlen=0, default=None, cls=None):
    """
    returns a list version of x if x is a non-string iterable, otherwise
    returns a list with x as its only element
    """
    if x is None:
        x = []
    elif not isinstance(x, list):
        x = list(x) if is_listy(x) else [x]

    if minlen and len(x) < minlen:
        x.extend([default for i in range(minlen - len(x))])

    if cls and type(x) is not cls:
        x = cls(x)
    return x


def mappify(x, default=True, cls=None):
    if not isinstance(x, Mapping):
        if isinstance(x, six.string_types):
            x = {x: default}
        elif isinstance(x, Iterable):
            x = dict([(v, default) for v in x])
        else:
            raise TypeError("Unable to mappify {0}".format(type(x)), x)

    if cls and type(x) is not cls:
        x = cls(x)
    return x
