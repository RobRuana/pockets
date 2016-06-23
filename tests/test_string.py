# -*- coding: utf-8 -*-
# Copyright (c) 2016 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""Tests for :mod:`pockets.string` module."""

from __future__ import absolute_import
import re
import sys

from unittest import TestCase

from pockets.string import camel, uncamel, splitcaps, UnicodeMixin
from six import u


class UnicodeMixinTest(TestCase):

    class ClassWithUnicode(UnicodeMixin):
        def __unicode__(self):
            if sys.version_info[0] >= 3:
                return 'ClassWithUnicode'
            else:
                return u'ClassWithUnicode'

    def test_unicode(self):
        obj = UnicodeMixinTest.ClassWithUnicode()
        self.assertEqual(obj.__unicode__(), u('ClassWithUnicode'))

    def test_str(self):
        obj = UnicodeMixinTest.ClassWithUnicode()
        self.assertEqual(obj.__str__(), 'ClassWithUnicode')


class UncamelTest(TestCase):
    def _run_tests(self, tests):
        for test_data in tests:
            test = test_data[0]
            expected = test_data[1]
            kwargs = (test_data[2] if len(test_data) > 2 else {})
            sep = kwargs.get("sep", "_")
            for pre in ("", " ", "  ", "   "):
                for post in ("", " ", "  ", "   "):
                    t = pre + test + post
                    e = pre + expected + post
                    actual = uncamel(t, **kwargs)
                    self.assertEqual(e, actual)
                    self.assertEqual(t.lower(), actual.replace(sep, ""))

    def test_uncamel(self):
        self._run_tests([
            ("", ""),
            ("T", "t"),
            ("TA", "ta"),
            ("TAQ", "taq"),
            ("TAsdf", "t_asdf"),
            ("TAZxcv", "ta_zxcv"),
            ("T TAsdf", "t t_asdf"),
            ("TAsdf TAsdf", "t_asdf t_asdf"),
            ("TAsdf Qwer TAsdf", "t_asdf qwer t_asdf"),
            ("Q TAsdf Q TAsdf Q", "q t_asdf q t_asdf q"),
            ("TAZxcv Qwer TA", "ta_zxcv qwer ta"),
            ("Test", "test"),
            ("TestAsdf", "test_asdf"),
            ("TestAsdfZxcv", "test_asdf_zxcv"),
            ("Test TestAsdf", "test test_asdf"),
            ("TestAsdf TestAsdf", "test_asdf test_asdf"),
            ("TestAsdf Qwer TestAsdf", "test_asdf qwer test_asdf"),
            ("TestAsdfZxcv Qwer TestAsdf", "test_asdf_zxcv qwer test_asdf"),
            ("Qwer TestAsdf Qwer TestAsdf Qwer",
             "qwer test_asdf qwer test_asdf qwer"),
            ("Test  TestAsdf", "test  test_asdf"),
            ("TestAsdf  TestAsdf", "test_asdf  test_asdf"),
            ("TestAsdf  Qwer  TestAsdf", "test_asdf  qwer  test_asdf"),
            ("Qwer  TestAsdf  Qwer  TestAsdf  Qwer",
             "qwer  test_asdf  qwer  test_asdf  qwer"),
            ("Test   TestAsdf", "test   test_asdf"),
            ("TestAsdf   TestAsdf", "test_asdf   test_asdf"),
            ("TestAsdf   Qwer   TestAsdf", "test_asdf   qwer   test_asdf"),
            ("Qwer   TestAsdf   Qwer   TestAsdf   Qwer",
             "qwer   test_asdf   qwer   test_asdf   qwer"),
        ])

    def test_uncamel_multiline(self):
        self._run_tests([
            ("""
             TestOne
             TestTwo
             """,
             """
             test_one
             test_two
             """)
        ])

    def test_sep(self):
        self._run_tests([
            ("", "", {"sep": ".*"}),
            ("T", "t", {"sep": ".*"}),
            ("TA", "ta", {"sep": ".*"}),
            ("TAQ", "taq", {"sep": ".*"}),
            ("TAsdf", "t.*asdf", {"sep": ".*"}),
            ("TAZxcv", "ta.*zxcv", {"sep": ".*"}),
            ("T TAsdf", "t t.*asdf", {"sep": ".*"}),
            ("TAsdf TAsdf", "t.*asdf t.*asdf", {"sep": ".*"}),
            ("TAsdf Qwer TAsdf", "t.*asdf qwer t.*asdf", {"sep": ".*"}),
            ("Q TAsdf Q TAsdf Q", "q t.*asdf q t.*asdf q", {"sep": ".*"}),
            ("TAZxcv Qwer TA", "ta.*zxcv qwer ta", {"sep": ".*"}),
            ("Test", "test", {"sep": ".*"}),
            ("TestAsdf", "test.*asdf", {"sep": ".*"}),
            ("TestAsdfZxcv", "test.*asdf.*zxcv", {"sep": ".*"}),
            ("Test TestAsdf", "test test.*asdf", {"sep": ".*"}),
            ("TestAsdf TestAsdf", "test.*asdf test.*asdf", {"sep": ".*"}),
            ("TestAsdf Qwer TestAsdf", "test.*asdf qwer test.*asdf",
             {"sep": ".*"}),
            ("TestAsdfZxcv Qwer TestAsdf",
             "test.*asdf.*zxcv qwer test.*asdf", {"sep": ".*"}),
            ("Qwer TestAsdf Qwer TestAsdf Qwer",
             "qwer test.*asdf qwer test.*asdf qwer", {"sep": ".*"}),
            ("Test  TestAsdf", "test  test.*asdf", {"sep": ".*"}),
            ("TestAsdf  TestAsdf", "test.*asdf  test.*asdf", {"sep": ".*"}),
            ("TestAsdf  Qwer  TestAsdf",
             "test.*asdf  qwer  test.*asdf", {"sep": ".*"}),
            ("Qwer  TestAsdf  Qwer  TestAsdf  Qwer",
             "qwer  test.*asdf  qwer  test.*asdf  qwer", {"sep": ".*"}),
            ("Test   TestAsdf", "test   test.*asdf", {"sep": ".*"}),
            ("TestAsdf   TestAsdf", "test.*asdf   test.*asdf", {"sep": ".*"}),
            ("TestAsdf   Qwer   TestAsdf",
             "test.*asdf   qwer   test.*asdf", {"sep": ".*"}),
            ("Qwer   TestAsdf   Qwer   TestAsdf   Qwer",
             "qwer   test.*asdf   qwer   test.*asdf   qwer", {"sep": ".*"}),
        ])

    def test_unicode(self):
        self._run_tests([
            (u("TeOneಠ-ಠ TeTwoಠ‿ಠ"), u("te_oneಠ-ಠ te_twoಠ‿ಠ")),
            (u("ಠ-ಠTeOneಠ-ಠ ಠ‿ಠTeTwoಠ‿ಠ"), u("ಠ-ಠ_te_oneಠ-ಠ ಠ‿ಠ_te_twoಠ‿ಠ"))
        ])


class CamelTest(TestCase):
    def _run_tests(self, tests):
        for test_data in tests:
            test = test_data[0]
            expected = test_data[1]
            kwargs = (test_data[2] if len(test_data) > 2 else {})
            sep = kwargs.get("sep", "_")
            for pre in ("", " ", "  ", "   ", sep, " " + sep + sep):
                for post in ("", " ", "  ", "   ", sep, " " + sep + sep):
                    t = pre + test + post
                    e = pre.replace(sep, "") + expected + post.replace(sep, "")
                    actual = camel(t, **kwargs)
                    self.assertEqual(e, actual)
                    self.assertEqual(t.replace(sep, "").lower(),
                                     actual.replace(sep, "").lower())

    def test_camel(self):
        self._run_tests([
            ("", ""),
            ("t", "T"),
            ("t_a", "TA"),
            ("t_a_q", "TAQ"),
            ("t_asdf", "TAsdf"),
            ("t_a_zxcv", "TAZxcv"),
            ("t t_asdf", "T TAsdf"),
            ("t_ t_asdf", "T TAsdf"),
            ("t_asdf t_asdf", "TAsdf TAsdf"),
            ("t_asdf_ t_asdf", "TAsdf TAsdf"),
            ("t_asdf_ qwer t_asdf", "TAsdf Qwer TAsdf"),
            ("q _t_asdf_ q t_asdf q", "Q TAsdf Q TAsdf Q"),
            ("t_a_zxcv qwer t_a", "TAZxcv Qwer TA"),
            ("test", "Test"),
            ("test_asdf", "TestAsdf"),
            ("test_asdf_zxcv", "TestAsdfZxcv"),
            ("test test_asdf", "Test TestAsdf"),
            ("test_ test_asdf", "Test TestAsdf"),
            ("test_asdf test_asdf", "TestAsdf TestAsdf"),
            ("test_asdf_ test_asdf", "TestAsdf TestAsdf"),
            ("test_asdf_ qwer test_asdf", "TestAsdf Qwer TestAsdf"),
            ("test_asdf_zxcv qwer test_asdf", "TestAsdfZxcv Qwer TestAsdf"),
            ("qwer _test_asdf_ qwer test_asdf qwer",
             "Qwer TestAsdf Qwer TestAsdf Qwer"),
            ("test  test_asdf", "Test  TestAsdf"),
            ("test_  test_asdf", "Test  TestAsdf"),
            ("test_asdf  test_asdf", "TestAsdf  TestAsdf"),
            ("test_asdf_  test_asdf", "TestAsdf  TestAsdf"),
            ("test_asdf_  qwer  test_asdf", "TestAsdf  Qwer  TestAsdf"),
            ("qwer  _test_asdf_  qwer  test_asdf  qwer",
             "Qwer  TestAsdf  Qwer  TestAsdf  Qwer"),
            ("test   test_asdf", "Test   TestAsdf"),
            ("test_   test_asdf", "Test   TestAsdf"),
            ("test_asdf   test_asdf", "TestAsdf   TestAsdf"),
            ("test_asdf_   test_asdf", "TestAsdf   TestAsdf"),
            ("test_asdf_   qwer   test_asdf", "TestAsdf   Qwer   TestAsdf"),
            ("qwer   _test_asdf_   qwer   test_asdf   qwer",
             "Qwer   TestAsdf   Qwer   TestAsdf   Qwer"),
            ("test", "Test"),
            ("test__asdf", "TestAsdf"),
            ("test__asdf__zxcv", "TestAsdfZxcv"),
            ("test test__asdf", "Test TestAsdf"),
            ("test__ test__asdf", "Test TestAsdf"),
            ("test__asdf test__asdf", "TestAsdf TestAsdf"),
            ("test__asdf__ test__asdf", "TestAsdf TestAsdf"),
            ("test__asdf__ test__asdf", "TestAsdf TestAsdf"),
            ("test_asdf__ qwer test__asdf", "TestAsdf Qwer TestAsdf"),
            ("qwer __test__asdf__ qwer test__asdf qwer",
             "Qwer TestAsdf Qwer TestAsdf Qwer"),
            ("test___asdf", "TestAsdf"),
            ("test___asdf___zxcv", "TestAsdfZxcv"),
            ("test test___asdf", "Test TestAsdf"),
            ("test___ test___asdf", "Test TestAsdf"),
            ("test___asdf test___asdf", "TestAsdf TestAsdf"),
            ("test___asdf___ test___asdf", "TestAsdf TestAsdf"),
            ("test___asdf___ test___asdf", "TestAsdf TestAsdf"),
            ("test_asdf___ qwer test___asdf", "TestAsdf Qwer TestAsdf"),
            ("qwer ___test___asdf___ qwer test___asdf qwer",
             "Qwer TestAsdf Qwer TestAsdf Qwer")
        ])

    def test_camel_multiline(self):
        self._run_tests([
            ("""
             test_one
             test_two
             """,
             """
             TestOne
             TestTwo
             """)
        ])

    def test_camel_non_alpha(self):
        self._run_tests([
            ("01t", "01t"),
            ("t01", "T01"),
            ("01t_a", "01tA"),
            ("t01_a", "T01A"),
            ("01t_a01_01q", "01tA0101q"),
            ("01_test01_01asdf", "01Test0101asdf"),
            ("01test_asdf_01zxcv", "01testAsdf01zxcv"),
            ("test 01test_asdf", "Test 01testAsdf"),
            ("test0_1as 01 t 01test_01asdf01", "Test01as 01 T 01test01asdf01"),
        ])

    def test_lower_initial_bool(self):
        self._run_tests([
            ("test", "Test", {"lower_initial": False}),
            ("test", "test", {"lower_initial": True}),
            ("tes_asd", "TesAsd", {"lower_initial": False}),
            ("tes_asd", "tesAsd", {"lower_initial": True}),
            ("01tes_asd", "01tesAsd", {"lower_initial": False}),
            ("01tes_asd", "01tesAsd", {"lower_initial": True}),
            ("01_tes_asd", "01TesAsd", {"lower_initial": False}),
            ("01_tes_asd", "01TesAsd", {"lower_initial": True}),
        ])

    def test_lower_initial_int(self):
        self._run_tests([
            ("test", "Test", {"lower_initial": 10}),
            ("test", "test", {"lower_initial": 0}),
            ("tes_asd", "TesAsd", {"lower_initial": -10}),
            ("tes_asd", "tesAsd", {"lower_initial": 0}),
            ("01tes_asd", "01tesAsd", {"lower_initial": 0}),
            ("01tes_asd", "01tesasd", {"lower_initial": 1}),
            ("01_tes_asd", "01TesAsd", {"lower_initial": 0}),
            ("01_tes_asd", "01tesAsd", {"lower_initial": 1}),
            ("01_tes_asd", "01Tesasd", {"lower_initial": -1}),
        ])

    def test_lower_initial_list(self):
        self._run_tests([
            ("tes_asd_zxc", "TesAsdZxc", {"lower_initial": []}),
            ("tes_asd_zxc", "tesAsdZxc", {"lower_initial": [0]}),
            ("tes_asd_zxc", "TesasdZxc", {"lower_initial": [1]}),
            ("tes_asd_zxc", "TesAsdzxc", {"lower_initial": [2]}),
            ("tes_asd_zxc", "TesAsdZxc", {"lower_initial": [3]}),
            ("tes_asd_zxc", "TesAsdZxc", {"lower_initial": [100]}),
            ("tes_asd_zxc", "TesAsdZxc", {"lower_initial": [-100]}),
            ("tes_asd_zxc", "TesAsdZxc", {"lower_initial": [-4]}),
            ("tes_asd_zxc", "tesAsdZxc", {"lower_initial": [-3]}),
            ("tes_asd_zxc", "TesasdZxc", {"lower_initial": [-2]}),
            ("tes_asd_zxc", "TesAsdzxc", {"lower_initial": [-1]}),
            ("tes_asd_zxc", "tesAsdzxc", {"lower_initial": [0, -1]}),
            ("tes_asd_zxc", "tesasdzxc", {"lower_initial": [0, 1, 2]}),
        ])

    def test_lower_initial_multiword(self):
        self._run_tests([
            ("test qwer", "Test Qwer", {"lower_initial": False}),
            ("test qwer", "test qwer", {"lower_initial": True}),
            ("tes_asd qwe", "TesAsd Qwe", {"lower_initial": False}),
            ("tes_asd qwe", "tesAsd qwe", {"lower_initial": True}),
            ("01tes_asd qwe_yugo", "01tesAsd QweYugo",
             {"lower_initial": False}),
            ("01tes_asd qwe_yugo", "01tesAsd qweYugo",
             {"lower_initial": True}),
            ("1_tes_asd qwe_yugo", "1TesAsd QweYugo",
             {"lower_initial": False}),
            ("1_tes_asd qwe_yugo", "1TesAsd qweYugo",
             {"lower_initial": True}),
        ])

    def test_lower_initial_preserve_upper(self):
        self._run_tests([
            ("teSt_aSdF", "TeStASdF",
             {"lower_initial": False, "preserve_upper": True}),
            ("teSt_aSdF", "TestAsdf",
             {"lower_initial": False, "preserve_upper": False}),
            ("teSt_aSdF", "teStASdF",
             {"lower_initial": True, "preserve_upper": True}),
            ("teSt_aSdF", "testAsdf",
             {"lower_initial": True, "preserve_upper": False}),
        ])

    def test_upper_segments(self):
        self._run_tests([
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": None}),
            ("tes_asd_zxc", "TESAsdZxc", {"upper_segments": 0}),
            ("tes_asd_zxc", "TesASDZxc", {"upper_segments": 1}),
            ("tes_asd_zxc", "TesAsdZXC", {"upper_segments": 2}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": 3}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": 1000}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": -1000}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": -4}),
            ("tes_asd_zxc", "TESAsdZxc", {"upper_segments": -3}),
            ("tes_asd_zxc", "TesASDZxc", {"upper_segments": -2}),
            ("tes_asd_zxc", "TesAsdZXC", {"upper_segments": -1}),
            ("tes_asd_zxc", "TESAsdZxc", {"upper_segments": [0]}),
            ("tes_asd_zxc", "TesASDZxc", {"upper_segments": [1]}),
            ("tes_asd_zxc", "TesAsdZXC", {"upper_segments": [2]}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": [3]}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": [1000]}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": [-1000]}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": [-4]}),
            ("tes_asd_zxc", "TESAsdZxc", {"upper_segments": [-3]}),
            ("tes_asd_zxc", "TesASDZxc", {"upper_segments": [-2]}),
            ("tes_asd_zxc", "TesAsdZXC", {"upper_segments": [-1]}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": [-4, 3]}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": [3, -4]}),
            ("tes_asd_zxc", "TESAsdZXC", {"upper_segments": [0, -1]}),
            ("tes_asd_zxc", "TESAsdZXC", {"upper_segments": [2, -3]}),
            ("tes_asd_zxc", "TesASDZxc", {"upper_segments": [1, -2]}),
            ("tes_asd_zxc", "TESASDZxc", {"upper_segments": [0, 1]}),
            ("tes_asd_zxc", "TesASDZXC", {"upper_segments": [1, 2]}),
            ("tes_asd_zxc", "TesASDZXC", {"upper_segments": [-2, -1]}),
            ("tes_asd_zxc", "TESASDZXC", {"upper_segments": [0, 1, 2]}),
            ("tes_asd_zxc", "TESASDZXC", {"upper_segments": [0, 1, -1]}),
            ("tes_asd_zxc", "TESASDZXC", {"upper_segments": [0, 2, -2]}),
            ("tes_asd_zxc", "TESASDZXC", {"upper_segments": [1, -1, -3]}),
            ("tes_asd_zxc", "TesASDZXC", {"upper_segments": [1, -1, -4]}),
            ("tes_asd_zxc", "TesASDZxc", {"upper_segments": [1, 3, -4]}),
            ("tes_asd_zxc", "TesAsdZxc", {"upper_segments": [100, 3, -4]}),
            ("tes_asd_zxc", "TESAsdZxc", {"upper_segments": [0, 0, 0]}),
            ("tes_asd_zxc", "TesASDZXC", {"upper_segments": [1, 2, 3, 4]}),
            ("tes_asd_zxc", "TESASDZXC", {"upper_segments": [0, 1, 2, 3, 4]}),
            ("tes_asd_zxc", "TesAsdZxc",
             {"upper_segments": [-5, -4, 3, 4, 5]}),
            ("tes_asd_zxc", "TESAsdZXC",
             {"upper_segments": [0, 2, 3, 4, 5, 6]})
        ])

    def test_upper_segments_multiword(self):
        self._run_tests([
            ("tes_asd_zxc qwe_yug_poi", "TESAsdZXC QWEYugPOI",
             {"upper_segments": [0, -1]}),
            ("tes_asd_zxc qwe_yug_poi", "TESAsdZXC QWEYugPOI",
             {"upper_segments": [2, -3]}),
            ("tes_asd_zxc qwe_yug_poi", "TesASDZxc QweYUGPoi",
             {"upper_segments": [1, -2]}),
            ("tes_asd_zxc qwe_yug_poi", "TESASDZxc QWEYUGPoi",
             {"upper_segments": [0, 1]}),
            ("tes_asd_zxc qwe_yug_poi", "TesASDZXC QweYUGPOI",
             {"upper_segments": [1, 2]}),
            ("tes_asd_zxc qwe_yug_poi", "TesASDZXC QweYUGPOI",
             {"upper_segments": [-2, -1]}),
            ("tes_asd_zxc qwe_yug_poi", "TESASDZXC QWEYUGPOI",
             {"upper_segments": [0, 1, 2]}),
        ])

    def test_preserve_upper(self):
        self._run_tests([
            ("teS_aSd_ZXC", "TeSASdZXC", {"preserve_upper": True}),
            ("teS_aSd_ZXC", "TesAsdZxc", {"preserve_upper": False}),
        ])

    def test_preserve_upper_multiword(self):
        self._run_tests([
            ("teS_aSd_ZXC qwe_YUG_poI", "TeSASdZXC QweYUGPoI",
             {"preserve_upper": True}),
            ("teS_aSd_ZXC qwe_YUG_poI", "TesAsdZxc QweYugPoi",
             {"preserve_upper": False}),
        ])

    def test_lower_upper_preserve(self):
        self._run_tests([
            ("xml_http_request", "xMLhTTPrEQUEST",
             {"lower_initial": [0, 1, 2],
              "upper_segments": [0, 1, 2],
              "preserve_upper": True}),
            ("xml_http_request", "xMLhTTPrEQUEST",
             {"lower_initial": [0, 1, 2],
              "upper_segments": [0, 1, 2],
              "preserve_upper": False}),
            ("Xml_Http_Request", "XMLHTTPREQUEST",
             {"lower_initial": [0, 1, 2],
              "upper_segments": [0, 1, 2],
              "preserve_upper": True}),
            ("Xml_Http_Request", "xMLhTTPrEQUEST",
             {"lower_initial": [0, 1, 2],
              "upper_segments": [0, 1, 2],
              "preserve_upper": False}),
        ])

    def test_sep(self):
        self._run_tests([
            ("tes_asd_zxc qwe-yug-poi", "TesAsdZxc Qwe-yug-poi",
             {"sep": "_"}),
            ("tes_asd_zxc qwe-yug-poi", "Tes_asd_zxc QweYugPoi",
             {"sep": "-"}),
            ("tes_asd_zxc qwe-yug-poi", "Tes_asd_zxcQwe-yug-poi",
             {"sep": " "}),
            ("tes_asd_zxc qwe-yug-poi", "Tes_asd_zxc Qwe-yug-poi",
             {"sep": "  "}),
            ("tes_asd_zxc  qwe-yug-poi", "Tes_asd_zxcQwe-yug-poi",
             {"sep": "  "}),
            ("tes_asd_zxc qwe-yug-poi", "Tes_asd_zxc Qwe--poi",
             {"sep": "yug"}),
        ])

    def test_unicode(self):
        O = u("ಠ").upper()
        self._run_tests([
            (u("te_one_ಠ_ಠ te_two‿ಠ‿ಠ"),
             u("TeOne") + O + O + u(" TeTwo‿ಠ‿ಠ")),
            (u("ಠ_ಠ_te_oneಠ_ಠ ಠ‿ಠte_twoಠ‿ಠ"),
             O + O + u("TeOneಠ") + O + u(" ") + O + u("‿ಠteTwoಠ‿ಠ"))
        ])


class SplitcapsTest(TestCase):
    def _run_tests(self, tests, split_initial_whitespace=False):
        for test_data in tests:
            test = test_data[0]
            expected = test_data[1]
            kwargs = (test_data[2] if len(test_data) > 2 else {})
            if "pattern" in kwargs or "flags" in kwargs:
                actual = splitcaps(test, **kwargs)
                self.assertEqual(expected, actual)
            else:
                for pre in ("", " ", "  ", "   "):
                    for post in ("", " ", "  ", "   "):
                        t = pre + test + post
                        e = list(expected)
                        if pre and split_initial_whitespace:
                            e = [pre] + e
                        else:
                            e[0] = pre + e[0]
                        e[-1] = e[-1] + post
                        actual = splitcaps(t, **kwargs)
                        self.assertEqual(e, actual)
                        self.assertEqual(t, "".join(actual))

    def test_splitcaps_initial_lowercase(self):
        self._run_tests([
            ("t", ["t"]),
            ("t01", ["t01"]),
            ("tX", ["t", "X"]),
            ("tX01", ["t", "X01"]),
            ("tOn", ["t", "On"]),
            ("tOn01", ["t", "On01"]),
            ("tXX", ["t", "XX"]),
            ("tXX01", ["t", "XX01"]),
            ("tXXOn", ["t", "XX", "On"]),
            ("tXXOn01", ["t", "XX", "On01"]),
            ("tXXXOn01", ["t", "XXX", "On01"]),
            ("tXX01On01", ["t", "XX01", "On01"]),
            ("tXXX01On01", ["t", "XXX01", "On01"]),
            ("test", ["test"]),
            ("test01", ["test01"]),
            ("testX", ["test", "X"]),
            ("test01X", ["test01", "X"]),
            ("testX01", ["test", "X01"]),
            ("testOne", ["test", "One"]),
            ("testOne01", ["test", "One01"]),
            ("testXX", ["test", "XX"]),
            ("testXX01", ["test", "XX01"]),
            ("testXXOne", ["test", "XX", "One"]),
            ("testXXOne01", ["test", "XX", "One01"]),
            ("testXXXOne01", ["test", "XXX", "One01"]),
            ("testXX01One01", ["test", "XX01", "One01"]),
            ("testXXX01One01", ["test", "XXX01", "One01"]),
        ])

    def test_splitcaps_initial_non_alpha(self):
        self._run_tests([
            ("1t", ["1t"]),
            ("1t01", ["1t01"]),
            ("1tX", ["1t", "X"]),
            ("1tX01", ["1t", "X01"]),
            ("1tOn", ["1t", "On"]),
            ("1tOn01", ["1t", "On01"]),
            ("1test", ["1test"]),
            ("1test01", ["1test01"]),
            ("1testX", ["1test", "X"]),
            ("1test01X", ["1test01", "X"]),
            ("1testX01", ["1test", "X01"]),
            ("1testOne", ["1test", "One"]),
            ("1testOne01", ["1test", "One01"]),
            ("1Tt", ["1", "Tt"]),
            ("1Tt01", ["1", "Tt01"]),
            ("1TtX", ["1", "Tt", "X"]),
            ("1TtX01", ["1", "Tt", "X01"]),
            ("1TtOn", ["1", "Tt", "On"]),
            ("1TtOn01", ["1", "Tt", "On01"]),
            ("1Ttest", ["1", "Ttest"]),
            ("1Ttest01", ["1", "Ttest01"]),
            ("1TtestX", ["1", "Ttest", "X"]),
            ("1Ttest01X", ["1", "Ttest01", "X"]),
            ("1TtestX01", ["1", "Ttest", "X01"]),
            ("1TtestOne", ["1", "Ttest", "One"]),
            ("1TtestOne01", ["1", "Ttest", "One01"]),
        ])

    def test_splitcaps_initial_uppercase(self):
        self._run_tests([
            ("X", ["X"]),
            ("X1", ["X1"]),
            ("X1X", ["X1X"]),
            ("X1XX", ["X1XX"]),
            ("X1X1X", ["X1X1X"]),
            ("X1X1Xt", ["X1X1", "Xt"]),
            ("X01", ["X01"]),
            ("X01X", ["X01X"]),
            ("X01XX", ["X01XX"]),
            ("X01X1X", ["X01X1X"]),
            ("X01X1Xt", ["X01X1", "Xt"]),
            ("X01Xt", ["X01", "Xt"]),
            ("X01XtX", ["X01", "Xt", "X"]),
            ("Xt", ["Xt"]),
            ("Xt01", ["Xt01"]),
            ("XtX", ["Xt", "X"]),
            ("XtX01", ["Xt", "X01"]),
            ("XtOn", ["Xt", "On"]),
            ("XtOn01", ["Xt", "On01"]),
            ("XtXX", ["Xt", "XX"]),
            ("XtXX01", ["Xt", "XX01"]),
            ("XtXXOn", ["Xt", "XX", "On"]),
            ("XtXXOn01", ["Xt", "XX", "On01"]),
            ("XtXX01On01", ["Xt", "XX01", "On01"]),
            ("Xtest", ["Xtest"]),
            ("Xtest01", ["Xtest01"]),
            ("XtestX", ["Xtest", "X"]),
            ("XtestX01", ["Xtest", "X01"]),
            ("XtestOne", ["Xtest", "One"]),
            ("XtestOne01", ["Xtest", "One01"]),
            ("XtestXX", ["Xtest", "XX"]),
            ("XtestXX01", ["Xtest", "XX01"]),
            ("XtestXXOne", ["Xtest", "XX", "One"]),
            ("XtestXXOne01", ["Xtest", "XX", "One01"]),
            ("XtestXX01One01", ["Xtest", "XX01", "One01"]),
            ("XX", ["XX"]),
            ("XX1", ["XX1"]),
            ("XX1X", ["XX1X"]),
            ("XX1XX", ["XX1XX"]),
            ("XX1X1X", ["XX1X1X"]),
            ("XX1X1Xt", ["XX1X1", "Xt"]),
            ("XX01", ["XX01"]),
            ("XX01X", ["XX01X"]),
            ("XX01XX", ["XX01XX"]),
            ("XX01X1X", ["XX01X1X"]),
            ("XX01X1Xt", ["XX01X1", "Xt"]),
            ("XX01t", ["X", "X01t"]),
            ("XX01Xt", ["XX01", "Xt"]),
            ("XX01XXt", ["XX01X", "Xt"]),
            ("XX01X1t", ["XX01", "X1t"]),
            ("XX01X1Xt", ["XX01X1", "Xt"]),
            ("XXt", ["X", "Xt"]),
            ("XXt01", ["X", "Xt01"]),
            ("XXtX", ["X", "Xt", "X"]),
            ("XXtX01", ["X", "Xt", "X01"]),
            ("XXtOn", ["X", "Xt", "On"]),
            ("XXtOn01", ["X", "Xt", "On01"]),
            ("XXtXX", ["X", "Xt", "XX"]),
            ("XXtXX01", ["X", "Xt", "XX01"]),
            ("XXtXXOn", ["X", "Xt", "XX", "On"]),
            ("XXtXXOn01", ["X", "Xt", "XX", "On01"]),
            ("XXtXX01On01", ["X", "Xt", "XX01", "On01"]),
            ("XXtest", ["X", "Xtest"]),
            ("XXtest01", ["X", "Xtest01"]),
            ("XXtestX", ["X", "Xtest", "X"]),
            ("XXtestX01", ["X", "Xtest", "X01"]),
            ("XXtestOne", ["X", "Xtest", "One"]),
            ("XXtestOne01", ["X", "Xtest", "One01"]),
            ("XXtestXX", ["X", "Xtest", "XX"]),
            ("XXtestXX01", ["X", "Xtest", "XX01"]),
            ("XXtestXXOne", ["X", "Xtest", "XX", "One"]),
            ("XXtestXXOne01", ["X", "Xtest", "XX", "One01"]),
            ("XXtestXX01One01", ["X", "Xtest", "XX01", "One01"]),
        ], split_initial_whitespace=True)

    def test_splitcaps_multiline(self):
        self._run_tests([
            ("""
             TestOne
             TestTwo
             """,
             ["""
             """,
              """Test""",
              """One
             """,
              """Test""",
              """Two
             """])
        ])

    def test_splitcaps_multiword(self):
        self._run_tests([
            ("asdf test", ["asdf test"]),
            ("asdf01 test01", ["asdf01 test01"]),
            ("asdfX testX", ["asdf", "X test", "X"]),
            ("asdf01X test01X", ["asdf01", "X test01", "X"]),
            ("asdfX01 testX01", ["asdf", "X01 test", "X01"]),
            ("asdfOne testOne", ["asdf", "One test", "One"]),
            ("asdfOne01 testOne01", ["asdf", "One01 test", "One01"]),
            ("asdfXX testXX", ["asdf", "X", "X test", "XX"]),
            ("asdfXX01 testXX01", ["asdf", "X", "X01 test", "XX01"]),
            ("asdfXXOne testXXOne",
             ["asdf", "XX", "One test", "XX", "One"]),
            ("asdfXXOne01 testXXOne01",
             ["asdf", "XX", "One01 test", "XX", "One01"]),
        ])

    def test_pattern(self):
        self._run_tests([
            ("asdf test", ["asdf test"], {"pattern": ""}),
            ("asdf test", ["asdf", "test"], {"pattern": "\s+"}),
            ("asdf test ", ["asdf", "test"], {"pattern": "\s+"}),
            ("asdf test", ["asdf test"], {"pattern": ""}),
            ("asdf test", ["asdf", " ", "test"], {"pattern": "(\s+)"}),
            ("asdf test ", ["asdf", " ", "test", " "], {"pattern": "(\s+)"}),
            ("ASDf Test", ["AS", "Df ", "Test"], {"pattern": ""}),
            ("ASDf Test", ["AS", "Df", "Test"], {"pattern": "\s+"}),
            ("ASDf Test", ["AS", "Df", " ", "Test"], {"pattern": "(\s+)"}),
            ("ASDf Test", ["AS", "Df ", "T", "t"],
             {"pattern": "es"}),
            ("ASDf Test", ["AS", "Df ", "T", "es", "t"],
             {"pattern": "(es)"}),
            ("ASDf Test", ["AS", "Df", "T", "t"],
             {"pattern": "\s|es"}),
            ("ASDf Test", ["AS", "Df", " ", "T", "es", "t"],
             {"pattern": "(\s|es)"}),
            ("ASDf Test", ["AS", "Df", " ", "T", "es", "t"],
             {"pattern": "(\s)|(es)"}),
        ])

    def test_maxsplit(self):
        self._run_tests([
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1Bb2Cc3Dd4Ee5Ff6"],
             {"maxsplit": 0}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2", "Cc3", "Dd4", "Ee5", "Ff6"],
             {"maxsplit": None}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2", "Cc3", "Dd4", "Ee5", "Ff6"],
             {"maxsplit": -1}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2", "Cc3", "Dd4", "Ee5", "Ff6"],
             {"maxsplit": -2}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2", "Cc3", "Dd4", "Ee5", "Ff6"],
             {"maxsplit": 10}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2", "Cc3", "Dd4", "Ee5", "Ff6"],
             {"maxsplit": 5}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2", "Cc3", "Dd4", "Ee5Ff6"],
             {"maxsplit": 4}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2", "Cc3", "Dd4Ee5Ff6"],
             {"maxsplit": 3}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2", "Cc3Dd4Ee5Ff6"],
             {"maxsplit": 2}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1", "Bb2Cc3Dd4Ee5Ff6"],
             {"maxsplit": 1}),
        ])

    def test_maxsplit_pattern(self):
        self._run_tests([
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa1Bb2Cc3Dd4Ee5Ff6"],
             {"maxsplit": 0, "pattern": "\d+"}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa", "Bb", "Cc", "Dd", "Ee", "Ff"],
             {"maxsplit": None, "pattern": "\d+"}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa", "Bb", "Cc", "Dd", "Ee", "Ff"],
             {"maxsplit": -1, "pattern": "\d+"}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa", "Bb", "Cc", "Dd", "Ee", "Ff"],
             {"maxsplit": -2, "pattern": "\d+"}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa", "Bb", "Cc", "Dd", "Ee", "Ff"],
             {"maxsplit": 12, "pattern": "\d+"}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa", "Bb", "Cc", "Dd", "Ee", "Ff"],
             {"maxsplit": 11, "pattern": "\d+"}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ["aa", "Bb", "Cc", "Dd", "Ee", "Ff"],
             {"maxsplit": 10, "pattern": "\d+"}),
            ("Aa1Bb2Cc3Dd4Ee5Ff6", ['Aa', 'Bb', 'Cc', 'Dd', 'Ee', 'Ff6'],
             {"maxsplit": 5, "pattern": "\d+"}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ['aa', 'Bb', 'Cc', 'Dd', 'Ee5Ff6'],
             {"maxsplit": 4, "pattern": "\d+"}),
            ("Aa1Bb2Cc3Dd4Ee5Ff6", ['Aa', 'Bb', 'Cc', 'Dd4Ee5Ff6'],
             {"maxsplit": 3, "pattern": "\d+"}),
            ("aa1Bb2Cc3Dd4Ee5Ff6", ['aa', 'Bb', 'Cc3Dd4Ee5Ff6'],
             {"maxsplit": 2, "pattern": "\d+"}),
            ("Aa1Bb2Cc3Dd4Ee5Ff6", ["Aa", "Bb2Cc3Dd4Ee5Ff6"],
             {"maxsplit": 1, "pattern": "\d+"})
        ])

    def test_maxsplit_pattern_group(self):
        self._run_tests([
            ("aa1Bb2Cc3Dd4Ee5", ["aa1Bb2Cc3Dd4Ee5"],
             {"maxsplit": 0, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5",
             ["aa", "1", "Bb", "2", "Cc", "3", "Dd", "4", "Ee", "5"],
             {"maxsplit": None, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5",
             ["aa", "1", "Bb", "2", "Cc", "3", "Dd", "4", "Ee", "5"],
             {"maxsplit": -1, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5",
             ["aa", "1", "Bb", "2", "Cc", "3", "Dd", "4", "Ee", "5"],
             {"maxsplit": -2, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5",
             ["aa", "1", "Bb", "2", "Cc", "3", "Dd", "4", "Ee", "5"],
             {"maxsplit": 10, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5", ["aa", "1", "Bb", "2", "Cc", "3Dd4Ee5"],
             {"maxsplit": 5, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5", ["aa", "1", "Bb", "2", "Cc3Dd4Ee5"],
             {"maxsplit": 4, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5", ["aa", "1", "Bb", "2Cc3Dd4Ee5"],
             {"maxsplit": 3, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5", ["aa", "1", "Bb2Cc3Dd4Ee5"],
             {"maxsplit": 2, "pattern": "(\d+)"}),
            ("aa1Bb2Cc3Dd4Ee5", ["aa", "1Bb2Cc3Dd4Ee5"],
             {"maxsplit": 1, "pattern": "(\d+)"}),
        ])

    def test_maxsplit_pattern_partial_group(self):
        self._run_tests([
            ("aa1_0Bb2_0Cc3_0Dd4_0",
             ["aa", "1", "0", "Bb", "2", "0", "Cc", "3", "0", "Dd", "4", "0"],
             {"pattern": "(\d)_(\d)"}),
            ("aa1_0Bb2_0Cc3_0Dd4_0",
             ["aa1_0", "Bb2_0", "Cc3_0", "Dd4_0"],
             {"pattern": "_(\d)_"}),
            ("aa1_0Bb2_0Cc3_0Dd4_0",
             ["aa", "_", "Bb", "_", "Cc", "_", "Dd", "_"],
             {"pattern": "\d(_)\d"}),
        ])

    def test_flags(self):
        self._run_tests([
            ("ASDf test", ["AS", "Df test"], {"flags": 0}),
            ("ASDf test", ["AS", "Df test"], {"flags": re.IGNORECASE}),
            ("ASDf test", ["f test"], {"pattern": "[A-Z]", "flags": 0}),
            ("ASDf test", ["A", "S", "D", "f test"],
             {"pattern": "([A-Z])", "flags": 0}),
            ("ASDf test", [" "],
             {"pattern": "[A-Z]", "flags": re.IGNORECASE}),
            ("ASDf test", ["A", "S", "D", "f", " ", "t", "e", "s", "t"],
             {"pattern": "([A-Z])", "flags": re.IGNORECASE}),
        ])
