# -*- coding: utf-8 -*-
# Copyright (c) 2017 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.logging` module."""

from __future__ import absolute_import
import logging

import pytest
from six import StringIO
from pockets.logging import log_exceptions, AutoLogger, \
    EagerFormattingAdapter, IndentMultilineLogFormatter


@pytest.fixture()
def log_stream(request):
    stream = StringIO()
    root = logging.getLogger()
    root.setLevel(logging.TRACE)
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.TRACE)
    formatter = IndentMultilineLogFormatter(
        '[%(levelname)s] %(name)s: %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    yield stream
    root.removeHandler(handler)


def test_autolog_from_function(log_stream):
    from pockets.autolog import log
    log.trace('TEST MSG')
    assert log_stream.getvalue() == '[TRACE] tests.test_logging: TEST MSG\n'


class TestAutoLogFromClass(object):
    def test_autolog_from_class(self, log_stream):
        from pockets.autolog import log
        log.trace('TEST MSG')
        assert log_stream.getvalue() == \
            '[TRACE] tests.test_logging.TestAutoLogFromClass: TEST MSG\n'


def test_log_exceptions(log_stream):

    @log_exceptions
    def raises_exception(*args, **kwargs):
        assert False

    pytest.raises(AssertionError, raises_exception, 'arg1', kwarg1='kwarg1')
    result = log_stream.getvalue()

    assert result.startswith("""\
[TRACE] pockets.logging: Calling tests.test_logging.raises_exception ['arg1'] {'kwarg1': 'kwarg1'}
[ERROR] pockets.logging: Error calling function raises_exception: assert False
[ERROR] pockets.logging: assert False
  Traceback (most recent call last):
""")  # noqa

    assert result.endswith("""\
  AssertionError: assert False
""")


def test_eager_formatting_adapter(log_stream):
    log = AutoLogger(EagerFormattingAdapter)
    log.log(0, 'suppressed')
    log.debug('a %(a)d b %(b)s', {'a': 1, 'b': 2})
    log.trace('TEST NO INTERPOLATION')
    log.trace('TEST %s', 'MSG')
    log.debug('TEST %s', 'MSG')
    log.info('TEST %s%s%s', 'M', 'S', 'G')
    log.warn('TEST %s', 'MSG')
    log.warning('TEST %s', 'MSG')
    log.error('TEST %s', 'MSG')
    try:
        assert False
    except:
        log.exception('TEST %s', 'MSG')
    log.critical('TEST %s', 'MSG')
    log.fatal('TEST %s', 'MSG')
    result = log_stream.getvalue()

    assert result.startswith("""\
[DEBUG] tests.test_logging: a 1 b 2
[TRACE] tests.test_logging: TEST NO INTERPOLATION
[TRACE] tests.test_logging: TEST MSG
[DEBUG] tests.test_logging: TEST MSG
[INFO] tests.test_logging: TEST MSG
[WARNING] tests.test_logging: TEST MSG
[WARNING] tests.test_logging: TEST MSG
[ERROR] tests.test_logging: TEST MSG
[ERROR] tests.test_logging: TEST MSG
  Traceback (most recent call last):
""")

    assert result.endswith("""\
  AssertionError: assert False
[CRITICAL] tests.test_logging: TEST MSG
[CRITICAL] tests.test_logging: TEST MSG
""")
