# -*- coding: utf-8 -*-
# Copyright (c) 2018 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.collections` module."""

from __future__ import absolute_import
from datetime import datetime, timedelta

import pytest
import pytz

from pockets.datetime import ceil_datetime, floor_datetime, round_datetime


NEW_YORK = pytz.timezone('America/New_York')


@pytest.mark.parametrize('dt,nearest,expected', [
    (
        datetime(2012, 12, 31, 23, 59, 31, 999999),
        timedelta(minutes=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 31),
        timedelta(minutes=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 30),
        timedelta(minutes=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 29),
        timedelta(minutes=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 31, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 30, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 29, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 31),
        timedelta(hours=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 30),
        timedelta(hours=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 29),
        timedelta(hours=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 31, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 30, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 29, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 13),
        timedelta(days=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 12),
        timedelta(days=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 11),
        timedelta(days=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 13, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 12, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 11, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
])
def test_ceil_datetime(dt, nearest, expected):
    assert ceil_datetime(dt, nearest) == expected


@pytest.mark.parametrize('dt,nearest,expected', [
    (
        datetime(2012, 12, 31, 23, 59, 31, 999999),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 31),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 30),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 29),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 31, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 30, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 29, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 31),
        timedelta(hours=1),
        datetime(2012, 12, 31, 23),
    ),
    (
        datetime(2012, 12, 31, 23, 30),
        timedelta(hours=1),
        datetime(2012, 12, 31, 23),
    ),
    (
        datetime(2012, 12, 31, 23, 29),
        timedelta(hours=1),
        datetime(2012, 12, 31, 23),
    ),
    (
        datetime(2012, 12, 31, 23, 31, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2012, 12, 31, 23, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 30, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2012, 12, 31, 23, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 29, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2012, 12, 31, 23, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 13),
        timedelta(days=1),
        datetime(2012, 12, 31),
    ),
    (
        datetime(2012, 12, 31, 12),
        timedelta(days=1),
        datetime(2012, 12, 31),
    ),
    (
        datetime(2012, 12, 31, 11),
        timedelta(days=1),
        datetime(2012, 12, 31),
    ),
    (
        datetime(2012, 12, 31, 13, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2012, 12, 31, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 12, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2012, 12, 31, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 11, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2012, 12, 31, tzinfo=NEW_YORK),
    ),
])
def test_floor_datetime(dt, nearest, expected):
    assert floor_datetime(dt, nearest) == expected


@pytest.mark.parametrize('dt,nearest,expected', [
    (
        datetime(2012, 12, 31, 23, 59, 31, 999999),
        timedelta(minutes=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 31),
        timedelta(minutes=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 30),
        timedelta(minutes=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 29),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 31, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 30, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 59, 29, tzinfo=NEW_YORK),
        timedelta(minutes=1),
        datetime(2012, 12, 31, 23, 59, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 31),
        timedelta(hours=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 30),
        timedelta(hours=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 23, 29),
        timedelta(hours=1),
        datetime(2012, 12, 31, 23),
    ),
    (
        datetime(2012, 12, 31, 23, 31, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 30, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 23, 29, tzinfo=NEW_YORK),
        timedelta(hours=1),
        datetime(2012, 12, 31, 23, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 13),
        timedelta(days=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 12),
        timedelta(days=1),
        datetime(2013, 1, 1),
    ),
    (
        datetime(2012, 12, 31, 11),
        timedelta(days=1),
        datetime(2012, 12, 31),
    ),
    (
        datetime(2012, 12, 31, 13, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 12, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2013, 1, 1, tzinfo=NEW_YORK),
    ),
    (
        datetime(2012, 12, 31, 11, tzinfo=NEW_YORK),
        timedelta(days=1),
        datetime(2012, 12, 31, tzinfo=NEW_YORK),
    ),
])
def test_round_datetime(dt, nearest, expected):
    assert round_datetime(dt, nearest) == expected
