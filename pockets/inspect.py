# -*- coding: utf-8 -*-
# Copyright (c) 2015, by the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""A pocket full of useful reflection functions!"""

from __future__ import absolute_import
import inspect

from pockets.collections import listify
from six import functools, string_types

__all__ = ["resolve"]


def resolve(name, modules=None):
    """Resolve a dotted name to an object (usually class, module, or function).

    If `name` is a string, attempt to resolve it according to Python
    dot notation, e.g. "path.to.MyClass". If `name` is anything other than a
    string, return it immediately:

    >>> resolve("calendar.TextCalendar")
    <class 'calendar.TextCalendar'>
    >>> resolve(object()) #doctest: +ELLIPSIS
    <object object at 0x...>

    Leading dots are allowed in `name`, but they are ignored; resolution will
    never traverse **up** the module path.

    If `modules` is specified, then resolution of `name` is restricted
    to the given modules. If `modules` is not specified, then resolution of
    `name` is first attempted absolutely, and then relative to the calling
    function's module:

    >>> resolve("pockets.camel") #doctest: +ELLIPSIS
    <function camel at 0x...>
    >>> resolve("pockets.camel", modules=["re", "six"]) #doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    ValueError: Unable to resolve 'pockets.camel' in modules: ['re', 'six']

    Args:
        name (str or object): A dotted name.

        modules (str or list, optional): A module or list of modules, under
            which to search for `name`.

    Returns:
        object: The object specified by `name`.

    Raises:
        ValueError: If `name` can't be resolved.

    """
    if not isinstance(name, string_types):
        return name

    obj_path = name.split('.')
    while not obj_path[0]:
        obj_path.pop(0)
    search_paths = []
    if modules:
        for module_path in listify(modules):
            search_paths.append(module_path.split('.') + obj_path)
    else:
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
