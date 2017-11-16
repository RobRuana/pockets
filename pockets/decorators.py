# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""A pocket full of useful decorators!"""

from functools import wraps


__all__ = ['cached_classproperty', 'cached_property', 'classproperty']


class cached_classproperty(property):
    """
    Like @cached_property except it works on classes instead of instances.
    """
    def __init__(self, fget, *arg, **kw):
        super(cached_classproperty, self).__init__(fget, *arg, **kw)
        self.__doc__ = fget.__doc__
        self.__fget_name__ = fget.__name__

    def __get__(desc, self, cls):
        cache_attr = '_cached_{0}_{1}'.format(desc.__fget_name__, cls.__name__)
        if not hasattr(cls, cache_attr):
            setattr(cls, cache_attr, desc.fget(cls))
        return getattr(cls, cache_attr)


def cached_property(func):
    """decorator for making readonly, memoized properties"""
    cache_attr = '_cached_{0}'.format(func.__name__)

    @property
    @wraps(func)
    def caching(self, *args, **kwargs):
        if not hasattr(self, cache_attr):
            setattr(self, cache_attr, func(self, *args, **kwargs))
        return getattr(self, cache_attr)
    return caching


class classproperty(property):
    """
    Decorator to create a read-only class property similar to classmethod.

    For whatever reason, the @property decorator isn't smart enough to
    recognize @classmethods and behaves differently on them than on instance
    methods.  This decorator may be used like to create a class-level property,
    useful for singletons and other one-per-class properties.

    This implementation is partially based on
    `sqlalchemy.util.langhelpers.classproperty`.

    Note:
        Class properties created by @classproperty are read-only. Any attempts
        to write to the property will erase the @classproperty, and the
        behavior of the underlying method will be lost.

    >>> class MyClass(object):
    ...     @classproperty
    ...     def myproperty(cls):
    ...         return '{0}.myproperty'.format(cls.__name__)
    >>> MyClass.myproperty
    'MyClass.myproperty'

    """
    def __init__(self, fget, *arg, **kw):
        super(classproperty, self).__init__(fget, *arg, **kw)
        self.__doc__ = fget.__doc__

    def __get__(desc, self, cls):
        return desc.fget(cls)

    def getter(self, fget):
        raise AttributeError('@classproperty.getter is not supported')

    def setter(self, fset):
        raise AttributeError('@classproperty.setter is not supported')

    def deleter(self, fdel):
        raise AttributeError('@classproperty.deleter is not supported')
