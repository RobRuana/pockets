# -*- coding: utf-8 -*-
# Copyright (c) 2018 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.collections` module."""

from __future__ import absolute_import, print_function

from collections import defaultdict, deque
from datetime import datetime as dt

try:
    from collections.abc import Sequence, Set
except ImportError:
    from collections import Sequence, Set

import pytest
import six
from six import u

from pockets.collections import (
    groupify,
    keydefaultdict,
    is_listy,
    listify,
    is_mappy,
    mappify,
    nesteddefaultdict,
    readable_join,
    uniquify,
)


class Reminder:
    def __init__(self, when, where, what):
        self.when = when
        self.where = where
        self.what = what

    def __repr__(self):
        return "Reminder({0.when}, {0.where}, {0.what})".format(self)

    def __eq__(self, value):
        if not value:
            return False
        try:
            return (
                self.when == value.when
                and self.where == value.where
                and self.what == value.what
            )
        except AttributeError:
            return False


reminders = [
    Reminder("Fri", "Home", "Eat cereal"),
    Reminder("Fri", "Work", "Feed Ivan"),
    Reminder("Sat", "Home", "Sleep in"),
    Reminder("Sat", "Home", "Play Zelda"),
    Reminder("Sun", "Home", "Sleep in"),
    Reminder("Sun", "Work", "Reset database"),
]


class TestKeydefaultdict(object):
    def test_keydefaultdict(self):
        def reverse_factory(missing_key):
            return "".join([s for s in reversed(missing_key)])

        d = keydefaultdict(reverse_factory)
        assert d["asdf"] == "fdsa"
        assert d["asdf"] == "fdsa"

        d["asdf"] = "asdf"
        assert d["asdf"] == "asdf"
        assert d["asdf"] == "asdf"

        assert d["fdsa"] == "asdf"

    def test_keydefaultdict_no_default_factory(self):
        d = keydefaultdict()
        pytest.raises(KeyError, d.__getitem__, "asdf")


class TestGroupify(object):
    @pytest.mark.parametrize(
        "items,keys,val_key,expected",
        [
            (
                reminders,
                None,
                None,
                [
                    Reminder("Fri", "Home", "Eat cereal"),
                    Reminder("Fri", "Work", "Feed Ivan"),
                    Reminder("Sat", "Home", "Sleep in"),
                    Reminder("Sat", "Home", "Play Zelda"),
                    Reminder("Sun", "Home", "Sleep in"),
                    Reminder("Sun", "Work", "Reset database"),
                ],
            ),
            (
                reminders,
                "when",
                None,
                {
                    "Fri": [
                        Reminder("Fri", "Home", "Eat cereal"),
                        Reminder("Fri", "Work", "Feed Ivan"),
                    ],
                    "Sat": [
                        Reminder("Sat", "Home", "Sleep in"),
                        Reminder("Sat", "Home", "Play Zelda"),
                    ],
                    "Sun": [
                        Reminder("Sun", "Home", "Sleep in"),
                        Reminder("Sun", "Work", "Reset database"),
                    ],
                },
            ),
            (
                reminders,
                ["when", "where"],
                None,
                {
                    "Fri": {
                        "Home": [Reminder("Fri", "Home", "Eat cereal")],
                        "Work": [Reminder("Fri", "Work", "Feed Ivan")],
                    },
                    "Sat": {
                        "Home": [
                            Reminder("Sat", "Home", "Sleep in"),
                            Reminder("Sat", "Home", "Play Zelda"),
                        ]
                    },
                    "Sun": {
                        "Home": [Reminder("Sun", "Home", "Sleep in")],
                        "Work": [Reminder("Sun", "Work", "Reset database")],
                    },
                },
            ),
            (
                reminders,
                ["when", "where"],
                "what",
                {
                    "Fri": {"Home": ["Eat cereal"], "Work": ["Feed Ivan"]},
                    "Sat": {"Home": ["Sleep in", "Play Zelda"]},
                    "Sun": {"Home": ["Sleep in"], "Work": ["Reset database"]},
                },
            ),
            (
                reminders,
                lambda r: "{0.when} - {0.where}".format(r),
                "what",
                {
                    "Fri - Home": ["Eat cereal"],
                    "Fri - Work": ["Feed Ivan"],
                    "Sat - Home": ["Sleep in", "Play Zelda"],
                    "Sun - Home": ["Sleep in"],
                    "Sun - Work": ["Reset database"],
                },
            ),
        ],
    )
    def test_groupify(self, items, keys, val_key, expected):
        assert groupify(items, keys, val_key) == expected


class TestIsListy(object):
    def test_sized_builtin(self):
        sized = [
            (),
            (1,),
            [],
            [1],
            set(),
            set([1]),
            frozenset(),
            frozenset([1]),
            bytearray(),
            bytearray(1),
        ]
        if six.PY2:
            sized.extend(
                [xrange(0), xrange(2), buffer(""), buffer("x")]
            )  # noqa: F821
        for x in sized:
            assert is_listy(x)

    def test_excluded(self):
        assert not is_listy({})
        assert not is_listy(u(""))
        assert not is_listy("")
        assert not is_listy(b"")

    def test_unsized_builtin(self):
        assert not is_listy(iter([]))
        assert not is_listy(i for i in range(2))

    def test_user_defined_types(self):
        class AlwaysEmptySequence(Sequence):
            def __len__(self):
                return 0

            def __getitem__(self, i):
                return [][i]

        assert is_listy(AlwaysEmptySequence())

        class AlwaysEmptySet(Set):
            def __len__(self):
                return 0

            def __iter__(self):
                return iter([])

            def __contains__(self, x):
                return False

        assert is_listy(AlwaysEmptySet())

    def test_miscellaneous(self):
        class Foo(object):
            pass

        for x in [0, 1, False, True, Foo, object, object()]:
            assert not is_listy(x)

    def test_none(self):
        assert not is_listy(None)

    def test_set(self):
        assert is_listy(set())
        assert is_listy(set(["a", "b", "c"]))

    def test_string(self):
        assert not is_listy("")
        assert not is_listy("test")
        assert not is_listy(u(""))
        assert not is_listy(u("test"))

    def test_tuple(self):
        assert is_listy(tuple())
        assert is_listy(("a", "b", "c"))

    def test_list(self):
        assert is_listy([])
        assert is_listy(["a", "b", "c"])

    def test_dict(self):
        assert not is_listy({})
        assert not is_listy({"a": "A"})

    def test_ordered_dict(self):
        try:
            from collections import OrderedDict
        except ImportError:
            pass
        else:
            assert not is_listy(OrderedDict())
            assert not is_listy(OrderedDict({"a": "A"}))

    def test_frozenset(self):
        assert is_listy(frozenset())
        assert is_listy(frozenset(["a", "b", "c"]))

    def test_object(self):
        assert not is_listy(object())


class TestListify(object):
    def test_default(self):
        assert [] == listify([], default=None)
        assert ["a"] == listify(["a"], minlen=1, default=None)
        assert ["a", None] == listify(["a"], minlen=2, default=None)
        assert ["a", None, None] == listify(["a"], minlen=3, default=None)

        assert [] == listify([], default="XXX")
        assert ["a"] == listify(["a"], minlen=1, default="XXX")
        assert ["a", "XXX"] == listify(["a"], minlen=2, default="XXX")
        assert ["a", "XXX", "XXX"] == listify(["a"], minlen=3, default="XXX")

    def test_cls(self):
        x = ["a"]
        y = listify(x)
        assert x == y
        assert x is y
        x.append("b")
        assert x == y

        x = ["a"]
        y = listify(x, cls=None)
        assert x == y
        assert x is y
        x.append("b")
        assert x == y

        class sublist(list):
            pass

        x = ["a"]
        y = listify(x, cls=sublist)
        assert isinstance(y, sublist)
        assert x == y
        assert x is not y
        x.append("b")
        assert x != y

        x = ["a"]
        y = listify(x, cls=deque)
        assert isinstance(y, deque)
        assert x == list(y)
        assert len(x) == len(y)
        assert x is not y
        x.append("b")
        assert x != list(y)
        assert len(x) != len(y)

    def test_minlen(self):
        assert [] == listify([])
        assert [] == listify([], minlen=None)
        assert [] == listify([], minlen=-1)
        assert [] == listify([], minlen=0)
        assert [None] == listify([], minlen=1)
        assert [None, None] == listify([], minlen=2)
        assert [None, None, None] == listify([], minlen=3)

        assert ["a"] == listify(["a"])
        assert ["a"] == listify(["a"], minlen=None)
        assert ["a"] == listify(["a"], minlen=-1)
        assert ["a"] == listify(["a"], minlen=0)
        assert ["a"] == listify(["a"], minlen=1)
        assert ["a", None] == listify(["a"], minlen=2)
        assert ["a", None, None] == listify(["a"], minlen=3)

        assert ["a", "b"] == listify(["a", "b"])
        assert ["a", "b"] == listify(["a", "b"], minlen=None)
        assert ["a", "b"] == listify(["a", "b"], minlen=-1)
        assert ["a", "b"] == listify(["a", "b"], minlen=0)
        assert ["a", "b"] == listify(["a", "b"], minlen=1)
        assert ["a", "b"] == listify(["a", "b"], minlen=2)
        assert ["a", "b", None] == listify(["a", "b"], minlen=3)
        assert ["a", "b", None, None] == listify(["a", "b"], minlen=4)

    def test_none(self):
        assert [] == listify(None)
        assert [] == listify(None, minlen=0)
        assert [None] == listify(None, minlen=1)
        assert [None, None] == listify(None, minlen=2)

    def test_falsey(self):
        assert [0] == listify(0)
        assert [0] == listify(0, minlen=0)
        assert [0] == listify(0, minlen=1)
        assert [0, None] == listify(0, minlen=2)

        assert [""] == listify("")
        assert [""] == listify("", minlen=0)
        assert [""] == listify("", minlen=1)
        assert ["", None] == listify("", minlen=2)

        assert [] == listify([])
        assert [] == listify([], minlen=0)
        assert [None] == listify([], minlen=1)
        assert [None, None] == listify([], minlen=2)

    def test_set(self):
        assert [] == listify(set())
        assert ["a"] == listify(set("a"))
        assert ["a", "b"] == sorted(listify(set(["a", "b"])))

    def test_string(self):
        assert [""] == listify("")
        assert ["a"] == listify("a")
        assert ["ab"] == listify("ab")

    def test_tuple(self):
        assert [] == listify(tuple())
        assert ["a"] == listify(tuple("a"))
        assert ["a", "b"] == listify(tuple(["a", "b"]))

    def test_list(self):
        assert [] == listify([])
        assert ["a"] == listify(["a"])
        assert ["a", "b"] == listify(["a", "b"])

    def test_list_identity(self):
        x = ["a"]
        y = listify(x)
        assert x == y
        assert x is y
        x.append("b")
        assert x == y

        class sublist(list):
            pass

        x = sublist("a")
        y = listify(x)
        assert x == y
        assert x is y
        x.append("b")
        assert x == y

        x = sublist("a")
        y = listify(x, cls=list)
        assert x == y
        assert x is y
        x.append("b")
        assert x == y

    def test_dict(self):
        assert [{}] == listify({})
        assert [{"a": "A"}] == listify({"a": "A"})
        assert [{"a": "A", "b": "B"}] == listify({"a": "A", "b": "B"})

    def test_object(self):
        a = object()
        assert [a] == listify(a)


class TestNesteddefaultdict(object):
    def test_nesteddefaultdict(self):
        d1 = nesteddefaultdict()
        assert isinstance(d1, defaultdict)
        d2 = d1["d"]
        assert isinstance(d2, defaultdict)
        d3 = d2["d"]
        assert isinstance(d3, defaultdict)


class TestReadableJoin(object):
    @pytest.mark.parametrize(
        "xs,args,expected",
        [
            ([], [], ""),
            (["foo"], [], "foo"),
            (["foo", "bar"], [], "foo and bar"),
            (["foo", "bar", "baz"], [], "foo, bar, and baz"),
            (
                ["foo", "  ", "", "bar", "", "  ", "baz"],
                [],
                "foo, bar, and baz",
            ),
            (["foo", "bar", "baz"], ["or"], "foo, bar, or baz"),
            (["foo", "bar", "baz"], ["or", ";"], "foo; bar; or baz"),
            (["foo", "bar", "baz"], ["but never"], "foo, bar, but never baz"),
        ],
    )
    def test_readable_join(self, xs, args, expected):
        assert readable_join(xs, *args) == expected


class TestIsMappy(object):
    @pytest.mark.parametrize(
        "x,expected",
        [
            (dict(), True),
            (defaultdict(list), True),
            (list(), False),
            (set(), False),
            ("string", False),
        ],
    )
    def test_splitify(self, x, expected):
        assert is_mappy(x) == expected


class TestMappify(object):
    def test_default(self):
        assert {"a": None} == mappify(["a"], default=None)
        assert {"a": None, "b": None} == mappify(["a", "b"], default=None)

        assert {"a": "XXX"} == mappify(["a"], default="XXX")
        assert {"a": "XXX", "b": "XXX"} == mappify(["a", "b"], default="XXX")

    def test_cls(self):
        x = {"a": "A"}
        y = mappify(x)
        assert x == y
        assert x is y
        x["a"] = "B"
        assert x == y

        x = {"a": "A"}
        y = mappify(x, cls=None)
        assert x == y
        assert x is y
        x["a"] = "B"
        assert x == y

        class subdict(dict):
            pass

        x = {"a": "A"}
        y = mappify(x, cls=subdict)
        assert isinstance(y, subdict)
        assert x == y
        assert x is not y
        x["a"] = "B"
        assert x != y

        x = {"a": "A"}
        y = mappify(x, cls=lambda x: defaultdict(list, x))
        assert isinstance(y, defaultdict)
        assert x == y
        assert x is not y
        x["a"] = "B"
        assert x != y

    def test_none(self):
        assert {} == mappify(None)

    def test_set(self):
        assert {} == mappify(set())
        assert {"a": True} == mappify(set("a"))
        assert {"a": True, "b": True} == mappify(set(["a", "b"]))

    def test_string(self):
        assert {"": True} == mappify("")
        assert {"a": True} == mappify("a")
        assert {"ab": True} == mappify("ab")

    def test_tuple(self):
        assert {} == mappify(tuple())
        assert {"a": True} == mappify(tuple("a"))
        assert {"a": True, "b": True} == mappify(tuple(["a", "b"]))

    def test_list(self):
        assert {} == mappify([])
        assert {"a": True} == mappify(["a"])
        assert {"a": True, "b": True} == mappify(["a", "b"])

    def test_dict(self):
        assert {} == mappify({})
        assert {"a": "A"} == mappify({"a": "A"})
        assert {"a": "A", "b": "B"} == mappify({"a": "A", "b": "B"})

    def test_dict_identity(self):
        x = {"a": "A"}
        y = mappify(x)
        assert x == y
        assert x is y
        x["a"] = "B"
        assert x == y

        class subdict(dict):
            pass

        x = subdict(a="B")
        y = mappify(x)
        assert x == y
        assert x is y
        x["a"] = "B"
        assert x == y

        x = subdict(a="B")
        y = mappify(x, cls=dict)
        assert x == y
        assert x is y
        x["a"] = "B"
        assert x == y

    def test_ordered_dict(self):
        try:
            from collections import OrderedDict
        except ImportError:
            pass
        else:
            assert {} == mappify(OrderedDict())
            assert {"a": "A"} == mappify(OrderedDict({"a": "A"}))

    def test_frozenset(self):
        assert {} == mappify(frozenset())
        assert {"a": True} == mappify(frozenset("a"))
        assert {"a": True, "b": True}, mappify(frozenset(["a", "b"]))

    def test_object(self):
        pytest.raises(TypeError, mappify, object)


class TestUniquify(object):
    def test_uniquify(self):
        pytest.raises(TypeError, uniquify, None)
        assert [] == uniquify([])
        assert ["a", "b", "c"] == uniquify(["a", "b", "c"])
        assert ["a"] == uniquify(["a", "a", "a", "a", "a", "a", "a", "a"])
        assert ["a", "b", "c", "d", "e"] == uniquify(
            ["a", "b", "a", "c", "a", "d", "a", "e"]
        )

    def test_callable_key(self):
        assert ["ASDF", "ZXCV"] == uniquify(
            ["ASDF", "asdf", "ZXCV", "zxcv"], key=str.lower
        )

    def test_string_key(self):
        assert [dt(2018, 1, 1, 9), dt(2018, 1, 2, 10)] == uniquify(
            [
                dt(2018, 1, 1, 9),
                dt(2018, 1, 1, 12),
                dt(2018, 1, 2, 10),
                dt(2018, 1, 2, 11),
            ],
            key="day",
        )

    def test_cls(self):
        x = ["a", "a"]
        y = uniquify(x, cls=deque)
        assert isinstance(y, deque)
        assert len(y) == 1
        assert y == deque("a")
