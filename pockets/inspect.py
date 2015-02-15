# -*- coding: utf-8 -*-
# Copyright 2015 Rob Ruana
# Licensed under the BSD License, see LICENSE file for details.

"""A collection of helpful reflection tools!"""

from __future__ import absolute_import
import inspect

from pockets.collections import listify
from six import functools, string_types

__all__ = ["resolve"]


def resolve(name, modules=None):
    """Resolve a dotted name to an object (usually class, module, or function).

    Supported naming formats include:
        1. path.to.module.method
        2. path.to.module.ClassName

    Parameters
    ----------
    name : str or object
        The name to resolve.
    modules : str or list of str, optional
        A module or list of modules.

    Returns:
      object: Returns the object, if found.  If not, propagates the error.

    Raises
    ------
    ValueError: If the object specified by "name" can't be resolved

    """
    if not isinstance(name, string_types):
        return name

    obj_path = name.split('.')
    search_paths = []
    for module_path in listify(modules):
        search_paths.append(module_path.split('.') + obj_path)
    search_paths.append(obj_path)
    caller = inspect.getouterframes(inspect.currentframe())[1][0].f_globals
    search_paths.append(caller['__name__'].split('.') + obj_path)

    for path in search_paths:
        try:
            obj = functools.reduce(getattr, path[1:], __import__(path[0]))
        except (AttributeError, ImportError):
            pass
        else:
            return obj

    raise ValueError("Unable to resolve '{0}' "
                     "in modules: {1}".format(name, modules))
