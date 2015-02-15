# -*- coding: utf-8 -*-
# Copyright 2015 Rob Ruana
# Licensed under the BSD License, see LICENSE file for details.

"""A collection of helpful Python tools!

*Let me check my pockets...*

"""


from __future__ import absolute_import, unicode_literals
from pockets._version import __version__
from pockets.collections import is_listy, listify, mappify
from pockets.inspect import resolve
from pockets.iterators import peek_iter, modify_iter
from pockets.string import camel, uncamel, splitcaps

__all__ = ["__version__",
           "is_listy",
           "listify",
           "mappify",
           "resolve",
           "peek_iter",
           "modify_iter",
           "camel",
           "uncamel",
           "splitcaps"]
