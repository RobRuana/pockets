# -*- coding: utf-8 -*-
# Copyright (c) 2018 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.iterators` module."""

from __future__ import absolute_import, print_function

import pytest
from six import u

from pockets.iterators import iterpeek, itermod


class BaseIteratorsTest(object):
    def assertEqualTwice(self, expected, func, *args):
        assert expected == func(*args)
        assert expected == func(*args)

    def assertFalseTwice(self, func, *args):
        assert not func(*args)
        assert not func(*args)

    def assertNext(self, it, expected, is_last):
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(expected, it.peek)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(expected, it.peek)
        self.assertTrueTwice(it.has_next)
        assert expected == next(it)
        if is_last:
            self.assertFalseTwice(it.has_next)
            self.assertRaisesTwice(StopIteration, it.next)
        else:
            self.assertTrueTwice(it.has_next)

    def assertRaisesTwice(self, exc, func, *args):
        pytest.raises(exc, func, *args)
        pytest.raises(exc, func, *args)

    def assertTrueTwice(self, func, *args):
        assert func(*args)
        assert func(*args)


class TestPeekIter(BaseIteratorsTest):
    def test_init_with_sentinel(self):
        a = iter(["1", "2", "DONE"])
        sentinel = "DONE"
        pytest.raises(TypeError, iterpeek, a, sentinel)

        def get_next():
            return next(a)

        it = iterpeek(get_next, sentinel)
        assert it.sentinel == sentinel
        self.assertNext(it, "1", is_last=False)
        self.assertNext(it, "2", is_last=True)

    def test_iter(self):
        a = ["1", "2", "3"]
        it = iterpeek(a)
        assert it is it.__iter__()

        a = []
        b = [i for i in iterpeek(a)]
        assert [] == b

        a = ["1"]
        b = [i for i in iterpeek(a)]
        assert ["1"] == b

        a = ["1", "2"]
        b = [i for i in iterpeek(a)]
        assert ["1", "2"] == b

        a = ["1", "2", "3"]
        b = [i for i in iterpeek(a)]
        assert ["1", "2", "3"] == b

    def test_next_with_multi(self):
        a = []
        it = iterpeek(a)
        self.assertFalseTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next, 2)

        a = ["1"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next, 2)
        self.assertTrueTwice(it.has_next)

        a = ["1", "2"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        assert ["1", "2"] == it.next(2)
        self.assertFalseTwice(it.has_next)

        a = ["1", "2", "3"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        assert ["1", "2"] == it.next(2)
        self.assertTrueTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next, 2)
        self.assertTrueTwice(it.has_next)

        a = ["1", "2", "3", "4"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        assert ["1", "2"] == it.next(2)
        self.assertTrueTwice(it.has_next)
        assert ["3", "4"] == it.next(2)
        self.assertFalseTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next, 2)
        self.assertFalseTwice(it.has_next)

    def test_next_with_none(self):
        a = []
        it = iterpeek(a)
        self.assertFalseTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next)
        self.assertFalseTwice(it.has_next)

        a = ["1"]
        it = iterpeek(a)
        assert "1" == it.__next__()

        a = ["1"]
        it = iterpeek(a)
        self.assertNext(it, "1", is_last=True)

        a = ["1", "2"]
        it = iterpeek(a)
        self.assertNext(it, "1", is_last=False)
        self.assertNext(it, "2", is_last=True)

        a = ["1", "2", "3"]
        it = iterpeek(a)
        self.assertNext(it, "1", is_last=False)
        self.assertNext(it, "2", is_last=False)
        self.assertNext(it, "3", is_last=True)

    def test_next_with_one(self):
        a = []
        it = iterpeek(a)
        self.assertFalseTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next, 1)

        a = ["1"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        assert ["1"] == it.next(1)
        self.assertFalseTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next, 1)

        a = ["1", "2"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        assert ["1"] == it.next(1)
        self.assertTrueTwice(it.has_next)
        assert ["2"] == it.next(1)
        self.assertFalseTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next, 1)

    def test_next_with_zero(self):
        a = []
        it = iterpeek(a)
        self.assertFalseTwice(it.has_next)
        self.assertRaisesTwice(StopIteration, it.next, 0)

        a = ["1"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice([], it.next, 0)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice([], it.next, 0)

        a = ["1", "2"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice([], it.next, 0)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice([], it.next, 0)

    def test_peek_with_multi(self):
        a = []
        it = iterpeek(a)
        self.assertFalseTwice(it.has_next)
        self.assertEqualTwice([it.sentinel, it.sentinel], it.peek, 2)
        self.assertFalseTwice(it.has_next)

        a = ["1"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1", it.sentinel], it.peek, 2)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1", it.sentinel, it.sentinel], it.peek, 3)
        self.assertTrueTwice(it.has_next)

        a = ["1", "2"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1", "2"], it.peek, 2)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1", "2", it.sentinel], it.peek, 3)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1", "2", it.sentinel, it.sentinel], it.peek, 4)
        self.assertTrueTwice(it.has_next)

        a = ["1", "2", "3"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1", "2"], it.peek, 2)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1", "2", "3"], it.peek, 3)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1", "2", "3", it.sentinel], it.peek, 4)
        self.assertTrueTwice(it.has_next)
        assert "1" == next(it)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["2", "3"], it.peek, 2)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["2", "3", it.sentinel], it.peek, 3)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["2", "3", it.sentinel, it.sentinel], it.peek, 4)
        self.assertTrueTwice(it.has_next)

    def test_peek_with_none(self):
        a = []
        it = iterpeek(a)
        self.assertFalseTwice(it.has_next)
        self.assertEqualTwice(it.sentinel, it.peek)
        self.assertFalseTwice(it.has_next)

        a = ["1"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice("1", it.peek)
        assert "1" == next(it)
        self.assertFalseTwice(it.has_next)
        self.assertEqualTwice(it.sentinel, it.peek)
        self.assertFalseTwice(it.has_next)

        a = ["1", "2"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice("1", it.peek)
        assert "1" == next(it)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice("2", it.peek)
        assert "2" == next(it)
        self.assertFalseTwice(it.has_next)
        self.assertEqualTwice(it.sentinel, it.peek)
        self.assertFalseTwice(it.has_next)

    def test_peek_with_one(self):
        a = []
        it = iterpeek(a)
        self.assertFalseTwice(it.has_next)
        self.assertEqualTwice([it.sentinel], it.peek, 1)
        self.assertFalseTwice(it.has_next)

        a = ["1"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1"], it.peek, 1)
        assert "1" == next(it)
        self.assertFalseTwice(it.has_next)
        self.assertEqualTwice([it.sentinel], it.peek, 1)
        self.assertFalseTwice(it.has_next)

        a = ["1", "2"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["1"], it.peek, 1)
        assert "1" == next(it)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice(["2"], it.peek, 1)
        assert "2" == next(it)
        self.assertFalseTwice(it.has_next)
        self.assertEqualTwice([it.sentinel], it.peek, 1)
        self.assertFalseTwice(it.has_next)

    def test_peek_with_zero(self):
        a = []
        it = iterpeek(a)
        self.assertFalseTwice(it.has_next)
        self.assertEqualTwice([], it.peek, 0)

        a = ["1"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice([], it.peek, 0)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice([], it.peek, 0)

        a = ["1", "2"]
        it = iterpeek(a)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice([], it.peek, 0)
        self.assertTrueTwice(it.has_next)
        self.assertEqualTwice([], it.peek, 0)


class TestModifyIter(BaseIteratorsTest):
    def test_init_with_sentinel_args(self):
        a = iter(["1", "2", "3", "DONE"])
        sentinel = "DONE"

        def get_next():
            return next(a)

        it = itermod(get_next, sentinel, int)
        expected = [1, 2, 3]
        assert expected == [i for i in it]

    def test_init_with_sentinel_kwargs(self):
        a = iter([1, 2, 3, 4])
        sentinel = 4

        def get_next():
            return next(a)

        it = itermod(get_next, sentinel, modifier=str)
        expected = ["1", "2", "3"]
        assert expected == [i for i in it]

    def test_modifier_default(self):
        a = ["", "  ", "  a  ", "b  ", "  c", "  ", ""]
        it = itermod(a)
        expected = ["", "  ", "  a  ", "b  ", "  c", "  ", ""]
        assert expected == [i for i in it]

    def test_modifier_not_callable(self):
        pytest.raises(TypeError, itermod, [1], modifier="not_callable")

    def test_modifier_rstrip(self):
        a = ["", "  ", "  a  ", "b  ", "  c", "  ", ""]
        it = itermod(a, modifier=lambda s: s.rstrip())
        expected = ["", "", "  a", "b", "  c", "", ""]
        assert expected == [i for i in it]

    def test_modifier_rstrip_unicode(self):
        a = [u(""), u("  "), u("  a  "), u("b  "), u("  c"), u("  "), u("")]
        it = itermod(a, modifier=lambda s: s.rstrip())
        expected = [u(""), u(""), u("  a"), u("b"), u("  c"), u(""), u("")]
        assert expected == [i for i in it]
