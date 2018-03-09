# -*- coding: utf-8 -*-
# Copyright (c) 2018 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""
*Let me check my pockets...*

Functions available in the `pockets.*` submodules are also imported to the base
package for easy access, so::

    from pockets import camel, iterpeek, resolve

works just as well as::

    from pockets.inspect import resolve
    from pockets.iterators import iterpeek
    from pockets.string import camel

"""

# flake8: noqa

from __future__ import absolute_import, print_function
from pockets._version import __version__
from pockets.collections import *
from pockets.datetime import *
from pockets.decorators import *
from pockets.inspect import *
from pockets.iterators import *
from pockets.logging import *
from pockets.string import *
