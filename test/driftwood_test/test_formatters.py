import json
import logging
import random
from unittest import mock, TestCase
import uuid

from nose2.tools import params

from driftwood.formatters import DictFormatter, JSONFormatter, KeyValFormatter
from driftwood_test import util

class TestDictFormatter:
    @params(*[{uuid.uuid4().hex:uuid.uuid4().hex for x in range(0,random.randrange(5,10))} for x in range(0,6)])
    def test_format_1(self, extra): 
        record = util.random_log_record(extra=extra)
        formatter = DictFormatter(extra_attrs=list(extra.keys()))
        dict_result = formatter.format(record)
        for key in util.regular_attrs:
            assert key in dict_result, "Result missing regular arg key '{0}'".format(key)
        for key in extra:
            assert key in dict_result, "Result missing extra arg key '{0}'".format(key)
        
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
        formatter = KeyValFormatter(regular_attrs = ["message", "created"])
        keyval_result = formatter.format(record)
        if keyval_result.startswith("message"):
            self.assertEquals(keyval_result, "message='{0}',created='{1}'".format(
                record.message, record.created))
        else:
            self.assertEquals(keyval_result, "created='{0}',message='{1}'".format(
                record.created, record.message)) 
        
        
