import json
import logging
import random
from unittest import mock
import uuid

from nose2.tools import params

from driftwood.formatters.json import JSONFormatter

def random_log_record(extra={}):
    handler = logging.Handler()
    handler.setLevel(logging.DEBUG)
    handler.emit = mock.MagicMock()
    log = logging.getLogger(uuid.uuid4().hex)
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    rand_level = logging.getLevelName(random.choice([10, 20, 30, 40, 50]))
    log_func = getattr(log, rand_level.lower())
    log_func(uuid.uuid4().hex, extra=extra)
    log_record =  handler.emit.call_args[0][0]
    log.removeHandler(handler)
    return log_record

class TestJSONFormatter:
    regular_attrs = ["name","levelno","levelname","pathname","filename","module","lineno",
        "funcName","created","msecs","relativeCreated","thread","threadName",
        "process"]

    @params(*[{uuid.uuid4().hex:uuid.uuid4().hex for x in range(0,random.randrange(5,10))} for x in range(0,6)])
    def test_format_1(self, extra):
        record = random_log_record(extra)
        formatter = JSONFormatter(extra_attrs=list(extra.keys()))
        json_result = formatter.format(record)
        dict_result = json.loads(json_result)
        for key in self.regular_attrs:
            assert key in dict_result, "Result missing regular arg key '{0}'".format(key)
        for key in extra:
            assert key in dict_result, "Result missing extra arg key '{0}'".format(key)
