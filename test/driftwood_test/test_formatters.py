import json
import logging
import random
from unittest import mock, TestCase
import uuid

import fauxfactory
from nose2.tools import params

from driftwood.formatters import DictFormatter, JSONFormatter, KeyValFormatter, SplunkFormatter
from driftwood_test import util

class TestDictFormatter(TestCase):
    @params(*[{uuid.uuid4().hex:uuid.uuid4().hex for x in range(0,random.randrange(5,10))} for x in range(0,6)])
    def test_format_1(self, extra): 
        record = util.random_log_record(extra=extra)
        formatter = DictFormatter(extra_attrs=list(extra.keys()))
        dict_result = formatter.format(record)
        for key in util.regular_attrs:
            assert key in dict_result, "Result missing regular arg key '{0}'".format(key)
        for key in extra:
            assert key in dict_result, "Result missing extra arg key '{0}'".format(key)

    def test_format_ordered_1(self):
        extra = {fauxfactory.gen_string("alphanumeric", random.randint(1,30)):fauxfactory.gen_string(
            "alphanumeric", random.randint(1,30)) for x in range(0, random.randint(4,8))}
        expected_order = sorted(list(extra.keys()), key=str.lower)
        record = util.random_log_record(extra=extra)
        formatter = DictFormatter(regular_attrs=["message"], preserve_order=True)
        dict_result = formatter.format(record)
        self.assertEqual("message", dict_result.popitem(last=False)[0])
        for key in expected_order:
            self.assertEqual(key, dict_result.popitem(last=False)[0])

    def test_format_ordered_2(self):
        record = util.random_log_record()
        formatter = DictFormatter( preserve_order=True, specific_order=["thread"])
        dict_result = formatter.format(record)
        self.assertEqual("thread", dict_result.popitem(last=False)[0])
        self.assertEqual(bool(len(dict_result) > 0), True)
        
class TestJSONFormatter:
    @params(*[{uuid.uuid4().hex:uuid.uuid4().hex for x in range(0,random.randrange(5,10))} for x in range(0,6)])
    def test_format_1(self, extra):
        record = util.random_log_record(extra=extra)
        formatter = JSONFormatter(extra_attrs=list(extra.keys()))
        json_result = formatter.format(record)
        dict_result = json.loads(json_result)
        for key in util.regular_attrs:
            assert key in dict_result, "Result missing regular arg key '{0}'".format(key)
        for key in extra:
            assert key in dict_result, "Result missing extra arg key '{0}'".format(key)

class TestKeyValFormatter(TestCase):
    def test_format_1(self):
        extra = {"foo":"bar"}
        record = util.random_log_record(extra)
        formatter = KeyValFormatter(extra_attrs=list(extra.keys()))
        keyval_result = formatter.format(record)
        for keyval_pair in [
            "foo='bar'",
            "message='{0}'".format(record.message),
            "created='{0}'".format(record.created)
        ]:
            assert keyval_pair in keyval_result, "Result \"{0}\" missing keyval pair {1}".format(
                keyval_result, keyval_pair)

    def test_format_2(self):
        record = util.random_log_record()
        record.foo = "bar"
        formatter = KeyValFormatter(regular_attrs = ["message", "created"], extra_attrs=["foo"])
        keyval_result = formatter.format(record)
        self.assertEqual(keyval_result, "message='{0}',created='{1}',foo='bar'".format(
            record.message, record.created))

class TestSplunkFormatter(TestCase):
    def test_format_1(self):
        formatter = SplunkFormatter()
        record = util.random_log_record()
        json_result = formatter.format(record)
        self.assertEqual(json_result.startswith('{"created"'), True)
