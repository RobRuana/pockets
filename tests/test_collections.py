# -*- coding: utf-8 -*-
# Copyright (c) 2016 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.collections` module."""

from __future__ import absolute_import
from collections import defaultdict, deque
from unittest import TestCase

from pockets.collections import is_listy, listify, mappify
from six import u


class BaseCollectionTestCase(TestCase):
    pass


class IsListyTest(BaseCollectionTestCase):
    def test_none(self):
        self.assertFalse(is_listy(None))

    def test_set(self):
        self.assertTrue(is_listy(set()))
        self.assertTrue(is_listy(set(["a", "b", "c"])))

    def test_string(self):
        self.assertFalse(is_listy(""))
        self.assertFalse(is_listy("test"))
        self.assertFalse(is_listy(u("")))
        self.assertFalse(is_listy(u("test")))

    def test_tuple(self):
        self.assertTrue(is_listy(tuple()))
        self.assertTrue(is_listy(("a", "b", "c")))

    def test_list(self):
        self.assertTrue(is_listy([]))
        self.assertTrue(is_listy(["a", "b", "c"]))

    def test_dict(self):
        self.assertFalse(is_listy({}))
        self.assertFalse(is_listy({"a": "A"}))

    def test_ordered_dict(self):
        try:
            from collections import OrderedDict
        except ImportError:
            pass
        else:
            self.assertFalse(is_listy(OrderedDict()))
            self.assertFalse(is_listy(OrderedDict({"a": "A"})))

    def test_frozenset(self):
        self.assertTrue(is_listy(frozenset()))
        self.assertTrue(is_listy(frozenset(["a", "b", "c"])))

    def test_object(self):
        self.assertFalse(is_listy(object()))


class ListifyTest(BaseCollectionTestCase):
    def test_default(self):
        self.assertEqual([], listify([], default=None))
        self.assertEqual(["a"], listify(["a"], minlen=1, default=None))
        self.assertEqual(["a", None], listify(["a"], minlen=2, default=None))
        self.assertEqual(["a", None, None], listify(["a"], minlen=3,
                         default=None))

        self.assertEqual([], listify([], default="XXX"))
        self.assertEqual(["a"], listify(["a"], minlen=1, default="XXX"))
        self.assertEqual(["a", "XXX"], listify(["a"], minlen=2,
                         default="XXX"))
        self.assertEqual(["a", "XXX", "XXX"], listify(["a"], minlen=3,
                         default="XXX"))

    def test_cls(self):
        x = ["a"]
        y = listify(x)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x.append("b")
        self.assertEqual(x, y)

        x = ["a"]
        y = listify(x, cls=None)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x.append("b")
        self.assertEqual(x, y)

        class sublist(list):
            pass

        x = ["a"]
        y = listify(x, cls=sublist)
        self.assertEqual(x, y)
        self.assertFalse(x is y)
        x.append("b")
        self.assertNotEqual(x, y)

        x = ["a"]
        y = listify(x, cls=deque)
        self.assertEqual(x, list(y))
        self.assertEqual(len(x), len(y))
        self.assertFalse(x is y)
        x.append("b")
        self.assertNotEqual(x, list(y))
        self.assertNotEqual(len(x), len(y))

    def test_minlen(self):
        self.assertEqual([], listify([]))
        self.assertEqual([], listify([], minlen=None))
        self.assertEqual([], listify([], minlen=-1))
        self.assertEqual([], listify([], minlen=0))
        self.assertEqual([None], listify([], minlen=1))
        self.assertEqual([None, None], listify([], minlen=2))
        self.assertEqual([None, None, None], listify([], minlen=3))

        self.assertEqual(["a"], listify(["a"]))
        self.assertEqual(["a"], listify(["a"], minlen=None))
        self.assertEqual(["a"], listify(["a"], minlen=-1))
        self.assertEqual(["a"], listify(["a"], minlen=0))
        self.assertEqual(["a"], listify(["a"], minlen=1))
        self.assertEqual(["a", None], listify(["a"], minlen=2))
        self.assertEqual(["a", None, None], listify(["a"], minlen=3))

        self.assertEqual(["a", "b"], listify(["a", "b"]))
        self.assertEqual(["a", "b"], listify(["a", "b"], minlen=None))
        self.assertEqual(["a", "b"], listify(["a", "b"], minlen=-1))
        self.assertEqual(["a", "b"], listify(["a", "b"], minlen=0))
        self.assertEqual(["a", "b"], listify(["a", "b"], minlen=1))
        self.assertEqual(["a", "b"], listify(["a", "b"], minlen=2))
        self.assertEqual(["a", "b", None], listify(["a", "b"], minlen=3))
        self.assertEqual(["a", "b", None, None], listify(["a", "b"], minlen=4))

    def test_none(self):
        self.assertEqual([], listify(None))
        self.assertEqual([], listify(None, minlen=0))
        self.assertEqual([None], listify(None, minlen=1))
        self.assertEqual([None, None], listify(None, minlen=2))

    def test_falsey(self):
        self.assertEqual([0], listify(0))
        self.assertEqual([0], listify(0, minlen=0))
        self.assertEqual([0], listify(0, minlen=1))
        self.assertEqual([0, None], listify(0, minlen=2))

        self.assertEqual([""], listify(""))
        self.assertEqual([""], listify("", minlen=0))
        self.assertEqual([""], listify("", minlen=1))
        self.assertEqual(["", None], listify("", minlen=2))

        self.assertEqual([], listify([]))
        self.assertEqual([], listify([], minlen=0))
        self.assertEqual([None], listify([], minlen=1))
        self.assertEqual([None, None], listify([], minlen=2))

    def test_set(self):
        self.assertEqual([], listify(set()))
        self.assertEqual(["a"], listify(set("a")))
        self.assertEqual(["a", "b"], sorted(listify(set(["a", "b"]))))

    def test_string(self):
        self.assertEqual([""], listify(""))
        self.assertEqual(["a"], listify("a"))
        self.assertEqual(["ab"], listify("ab"))

    def test_tuple(self):
        self.assertEqual([], listify(tuple()))
        self.assertEqual(["a"], listify(tuple("a")))
        self.assertEqual(["a", "b"], listify(tuple(["a", "b"])))

    def test_list(self):
        self.assertEqual([], listify([]))
        self.assertEqual(["a"], listify(["a"]))
        self.assertEqual(["a", "b"], listify(["a", "b"]))

    def test_list_identity(self):
        x = ["a"]
        y = listify(x)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x.append("b")
        self.assertEqual(x, y)

        class sublist(list):
            pass

        x = sublist("a")
        y = listify(x)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x.append("b")
        self.assertEqual(x, y)

        x = sublist("a")
        y = listify(x, cls=list)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x.append("b")
        self.assertEqual(x, y)

    def test_dict(self):
        self.assertEqual([{}], listify({}))
        self.assertEqual([{"a": "A"}], listify({"a": "A"}))
        self.assertEqual([{"a": "A", "b": "B"}], listify({"a": "A", "b": "B"}))

    def test_object(self):
        a = object()
        self.assertEqual([a], listify(a))


class MappifyTest(BaseCollectionTestCase):
    def test_default(self):
        self.assertEqual({"a": None}, mappify(["a"], default=None))
        self.assertEqual({"a": None, "b": None}, mappify(["a", "b"],
                         default=None))

        self.assertEqual({"a": "XXX"}, mappify(["a"], default="XXX"))
        self.assertEqual({"a": "XXX", "b": "XXX"}, mappify(["a", "b"],
                         default="XXX"))

    def test_cls(self):
        x = {"a": "A"}
        y = mappify(x)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x["a"] = "B"
        self.assertEqual(x, y)

        x = {"a": "A"}
        y = mappify(x, cls=None)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x["a"] = "B"
        self.assertEqual(x, y)

        class subdict(dict):
            pass

        x = {"a": "A"}
        y = mappify(x, cls=subdict)
        self.assertEqual(x, y)
        self.assertFalse(x is y)
        x["a"] = "B"
        self.assertNotEqual(x, y)

        x = {"a": "A"}
        y = mappify(x, cls=lambda x: defaultdict(list, x))
        self.assertEqual(x, y)
        self.assertFalse(x is y)
        x["a"] = "B"
        self.assertNotEqual(x, y)

    def test_none(self):
        self.assertRaises(TypeError, mappify, None)

    def test_set(self):
        self.assertEqual({}, mappify(set()))
        self.assertEqual({"a": True}, mappify(set("a")))
        self.assertEqual({"a": True, "b": True}, mappify(set(["a", "b"])))

    def test_string(self):
        self.assertEqual({"": True}, mappify(""))
        self.assertEqual({"a": True}, mappify("a"))
        self.assertEqual({"ab": True}, mappify("ab"))

    def test_tuple(self):
        self.assertEqual({}, mappify(tuple()))
        self.assertEqual({"a": True}, mappify(tuple("a")))
        self.assertEqual({"a": True, "b": True}, mappify(tuple(["a", "b"])))

    def test_list(self):
        self.assertEqual({}, mappify([]))
        self.assertEqual({"a": True}, mappify(["a"]))
        self.assertEqual({"a": True, "b": True}, mappify(["a", "b"]))

    def test_dict(self):
        self.assertEqual({}, mappify({}))
        self.assertEqual({"a": "A"}, mappify({"a": "A"}))
        self.assertEqual({"a": "A", "b": "B"}, mappify({"a": "A", "b": "B"}))

    def test_dict_identity(self):
        x = {"a": "A"}
        y = mappify(x)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x["a"] = "B"
        self.assertEqual(x, y)

        class subdict(dict):
            pass

        x = subdict(a="B")
        y = mappify(x)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x["a"] = "B"
        self.assertEqual(x, y)

        x = subdict(a="B")
        y = mappify(x, cls=dict)
        self.assertEqual(x, y)
        self.assertTrue(x is y)
        x["a"] = "B"
        self.assertEqual(x, y)

    def test_ordered_dict(self):
        try:
            from collections import OrderedDict
        except ImportError:
            pass
        else:
            self.assertEqual({}, mappify(OrderedDict()))
            self.assertEqual({"a": "A"}, mappify(OrderedDict({"a": "A"})))

    def test_frozenset(self):
        self.assertEqual({}, mappify(frozenset()))
        self.assertEqual({"a": True}, mappify(frozenset("a")))
        self.assertEqual({"a": True, "b": True},
                         mappify(frozenset(["a", "b"])))

    def test_object(self):
        self.assertRaises(TypeError, mappify, object)
