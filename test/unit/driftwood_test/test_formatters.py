import json
import logging
import random
from unittest import mock
import uuid

from nose2.tools import params

from driftwood.formatters import DictFormatter, JSONFormatter
from driftwood_test import util

class TestDictFormatter:
    @params(*[{uuid.uuid4().hex:uuid.uuid4().hex for x in range(0,random.randrange(5,10))} for x in range(0,6)])
    def test_format_1(self, extra): 
        record = util.random_log_record(extra)
        formatter = DictFormatter(extra_attrs=list(extra.keys()))
        dict_result = formatter.format(record)
        for key in util.regular_attrs:
            assert key in dict_result, "Result missing regular arg key '{0}'".format(key)
        for key in extra:
            assert key in dict_result, "Result missing extra arg key '{0}'".format(key)
        
class TestJSONFormatter:
    @params(*[{uuid.uuid4().hex:uuid.uuid4().hex for x in range(0,random.randrange(5,10))} for x in range(0,6)])
    def test_format_1(self, extra):
        record = util.random_log_record(extra)
        formatter = JSONFormatter(extra_attrs=list(extra.keys()))
        json_result = formatter.format(record)
        dict_result = json.loads(json_result)
        for key in util.regular_attrs:
            assert key in dict_result, "Result missing regular arg key '{0}'".format(key)
        for key in extra:
            assert key in dict_result, "Result missing extra arg key '{0}'".format(key)
