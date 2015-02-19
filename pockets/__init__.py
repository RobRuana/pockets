# -*- coding: utf-8 -*-
# Copyright (c) 2015, by the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""A collection of helpful Python tools!

*Let me check my pockets...*

"""

from __future__ import absolute_import
from pockets._version import __version__
from pockets.collections import is_listy, listify, mappify
from pockets.inspect import resolve
from pockets.iterators import peek_iter, modify_iter
from pockets.string import camel, uncamel, splitcaps


__all__ = ["__version__",
           "camel",
           "uncamel",
           "splitcaps",
           "resolve",
           "is_listy",
           "listify",
           "mappify",
           "peek_iter",
           "modify_iter"]
