# -*- coding: utf-8 -*-
# Copyright 2015 Rob Ruana
# Licensed under the BSD License, see LICENSE file for details.

"""A collection of helpful string manipulation tools!"""

from __future__ import absolute_import
import re

from pockets.collections import listify

__all__ = ["camel", "uncamel", "splitcaps"]

# Default regular expression flags
_re_flags = re.L | re.M | re.U

_whitespace_group_re = re.compile("(\s+)", _re_flags)

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
    ")", _re_flags)

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
_splitcaps_re = re.compile(_splitcaps_template.format("", "", ""), _re_flags)


def camel(s, sep="_", cap_initial=True, cap_segments=None,
          preserve_caps=True):
    """Converts underscore_separated string (aka snake_case) to CamelCase.

    Args:
        sep (string, optional): Defaults to "_".
        cap_initial (bool, optional): Defaults to True.
        cap_segments (int or list, optional): Defaults to None.
        preserve_caps (bool): Defaults to True.

    Returns:
        str: Camelized string.

    Example:
        >>> camel("xml_http_request")
        'XmlHttpRequest'
        >>> camel("xml_http_request", cap_segments=1)
        'XmlHTTPRequest'
        >>> camel("xml_http_request", cap_segments=[0, -1])
        'XMLHttpREQUEST'
        >>> camel("xml_http_request", cap_initial=False, cap_segments=1)
        'xmlHTTPRequest'

    """
    cap_segments = listify(cap_segments)
    result = []
    for word in _whitespace_group_re.split(s):
        segments = [segment for segment in word.split(sep) if segment]
        count = len(segments)
        for i, segment in enumerate(segments):
            if i in cap_segments or (i - count) in cap_segments:
                result.append(segment.upper())
            elif not cap_initial and i == 0:
                if preserve_caps:
                    result.append(segment)
                else:
                    result.append(segment.lower())
            else:
                if preserve_caps:
                    result.append(segment[0].upper())
                    result.append(segment[1:])
                else:
                    result.append(segment.title())

    return "".join(result)


def uncamel(s, sep="_"):
    """Convert CamelCase string to underscore_separated (aka snake_case).

    Args:
        sep (str, optional): Defaults to "_".

    Returns:
        str: Uncamelized string.

    Example:
        >>> uncamel("XmlHTTPRequest")
        'xml_http_request'
        >>> uncamel("XmlHTTPRequest", sep="-")
        'xml-http-request'

    """
    return _uncamel_re.sub(sep + r'\1', s).lower()


def splitcaps(s, pattern=None, maxsplit=0, flags=0):
    """Intelligently split a string on capital letters.

    Args:
        s (str): The string to split.
        pattern (str, optional): In addition to splitting on capital letters,
            also split by the occurrences of pattern. If capturing parentheses
            are used in pattern, then the text of all groups in the pattern are
            also returned as part of the resulting list. Defaults to None.

            splitcaps does not split on whitespace by default. If you want to
            also split on whitespace, pass "\\s+" for `pattern`:

                >>> splitcaps("Without whiteSpace pattern")
                ['Without white', 'Space pattern']
                >>> splitcaps("With whiteSpace pattern", pattern="\s+")
                ['With', 'white', 'Space', 'pattern']

        maxsplit (int, optional): The maximum number of splits to make.
        flags (int, optional): Flags to pass to the regular expression

    Returns:
        list: Capitalized substrings.

    """
    if pattern:
        if flags:
            r = re.compile(_splitcaps_pattern.format(pattern), flags)
        else:
            r = re.compile(_splitcaps_pattern.format(pattern), _re_flags)
    elif flags:
        r = re.compile(_splitcaps_re.pattern, flags)
    else:
        r = _splitcaps_re

    result = []
    for m in r.finditer(s):
        if len(m.groups()) != 1 or m.group(1) is None:
            result.append(m.group())
        if maxsplit > 0 and len(result) >= maxsplit:
            if m.end() < len(s):
                result.append(s[m.end():])
            break
    return result or [s]
