# -*- coding: utf-8 -*-
# Copyright 2015 Rob Ruana
# Licensed under the BSD License, see LICENSE file for details.

"""A collection of helpful string manipulation tools!"""

from __future__ import absolute_import
import re

from pockets.collections import listify

__all__ = ["camel", "uncamel", "splitcaps"]

_def_flags = re.L | re.M | re.U

_whitespace_group_re = re.compile("(\s+)", _def_flags)

_uncamel_re = re.compile(
    "("  # The whole expression is in a single group
    # Clause 1
    "(?<=[^\sA-Z])"  # Preceded by neither a space nor a capital letter
    "[A-Z]+[^a-z\s]*"  # All non-lowercase beginning with a capital letter
    "(?=[A-Z][^A-Z\s]*?[a-z]|\s|$)"  # Followed by a capitalized word
    "|"
    # Clause 2
    "(?<=[^\s])"  # Preceded by a character that is not a space
    "[A-Z][^A-Z\s]*?[a-z]+[^A-Z\s]*"  # Capitalized word
    ")", _def_flags)

_splitcaps_template = (
    # Clause 1
    "{0}"  # Leading instances of supplied pattern separator
    # Clause 2
    "[A-Z]+[^a-z{2}]*"  # All non-lowercase beginning with a capital letter
    "(?=[A-Z][^A-Z{2}]*?[a-z]|{1}$)"  # Followed by a capitalized word
    "|"
    # Clause 3
    "[A-Z][^A-Z{2}]*?[a-z]+[^A-Z{2}]*"  # Capitalized word
    "|"
    # Clause 4
    "[^A-Z{2}]+")  # All non-uppercase

_splitcaps_pattern = _splitcaps_template.format("({0})|", "{0}|", "{0}")
_splitcaps_re = re.compile(_splitcaps_template.format("", "", ""), _def_flags)


def camel(value, sep="_", cap_initial=True, cap_segments=None,
          preserve_caps=True):
    """Converts underscore_separated string (aka snake_case) to CamelCase.

    >>> camel("foo_bar_baz")
    'FooBarBaz'
    >>> camel("foo_bar_baz", cap_segments=0)
    'FOOBarBaz'
    >>> camel("foo_bar_baz", cap_segments=1)
    'FooBARBaz'
    >>> camel("foo_bar_baz", cap_segments=1000)
    'FooBarBaz'

    """
    cap_segments = listify(cap_segments)
    result = []
    for word in _whitespace_group_re.split(value):
        segments = [s for s in word.split(sep) if s]
        count = len(segments)
        for i, s in enumerate(segments):
            if i in cap_segments or (i - count) in cap_segments:
                result.append(s.upper())
            elif not cap_initial and i == 0:
                if preserve_caps:
                    result.append(s)
                else:
                    result.append(s.lower())
            else:
                if preserve_caps:
                    result.append(s[0].upper())
                    result.append(s[1:])
                else:
                    result.append(s.title())

    return "".join(result)


def uncamel(value, sep="_"):
    """Convert camelCase string to underscore_separated (aka snake_case).

    >>> uncamel("fooBarBaz")
    'foo_bar_baz'
    >>> uncamel("FooBarBazXYZ")
    'foo_bar_baz_xyz'

    """
    return _uncamel_re.sub(sep + r'\1', value).lower()


def splitcaps(value, pattern=None, maxsplit=0, flags=0):
    """Intelligently split a string on capital letters.

    Parameters
    ----------
    value : str
        The string to split.
    patter : str
        In addition to splitting on capital letters, also split by the
        occurrences of pattern. If capturing parentheses are used in pattern,
        then the text of all groups in the pattern are also returned as part
        of the resulting list.

    Returns
    -------
    list
        The matching substrings.

    """
    if pattern:
        if flags:
            r = re.compile(_splitcaps_pattern.format(pattern), flags)
        else:
            r = re.compile(_splitcaps_pattern.format(pattern), _def_flags)
    elif flags:
        r = re.compile(_splitcaps_re.pattern, flags)
    else:
        r = _splitcaps_re

    result = []
    for m in r.finditer(value):
        if len(m.groups()) != 1 or m.group(1) is None:
            result.append(m.group())
        if maxsplit > 0 and len(result) >= maxsplit:
            if m.end() < len(value):
                result.append(value[m.end():])
            break
    return result or [value]
