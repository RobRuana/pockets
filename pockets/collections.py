# -*- coding: utf-8 -*-
# Copyright 2015 Rob Ruana
# Licensed under the BSD License, see LICENSE file for details.

"""A collection of helpful collection tools!"""

from __future__ import absolute_import
from collections import Sized, Iterable, Mapping

import six

__all__ = ["is_listy", "listify", "mappify"]


def is_listy(x):
    """
    returns a boolean indicating whether the passed object is "listy",
    which we define as a sized iterable which is not a map or string
    """
    return (isinstance(x, Sized)
            and isinstance(x, Iterable)
            and not isinstance(x, Mapping)
            and not isinstance(x, six.string_types))


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
