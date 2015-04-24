import importlib
import json
import logging
import random
from unittest import mock
import uuid

from nose2.tools import params

from driftwood.handlers import DictHandler
import driftwood.handlers.mongo

from . import util

class TestDictHandler:
    @params(*[{uuid.uuid4().hex:uuid.uuid4().hex for x in range(0,random.randrange(5,10))} for x in range(0,6)])
    def test_1(self, extra): 
        record = util.random_log_record(extra)
        handler = DictHandler(extra_attrs=list(extra.keys()))
        dict_result = handler.emit(record)
        for key in util.regular_attrs:
            assert key in dict_result, "Result missing regular arg key '{0}'".format(key)
        for key in extra:
            assert key in dict_result, "Result missing extra arg key '{0}'".format(key)

class TestMongoHandler:
    @params(*[{uuid.uuid4().hex:uuid.uuid4().hex for x in range(0,random.randrange(5,10))} for x in range(0,6)])
    def test_generic_1(self, extra): 
        record = util.random_log_record(extra)
        handler = driftwood.handlers.mongo.MongoHandler(extra_attrs=list(extra.keys()))
        assert handler.document.__name__ == "LogRecord"
        mock_doc = mock.MagicMock()
        handler.document = mock.MagicMock(return_value=mock_doc)
        handler.emit(record)
        for key in util.regular_attrs:
            assert type(getattr(mock_doc, key)).__name__ != "MagicMock", \
                "Attribute not assigned '{0}'".format(key)
        for extra_key, extra_val in extra.items():
            assert getattr(mock_doc, extra_key) == extra_val, \
                "Attribute '{0}' not set to {1}".format(extra_key, extra_val)
        mock_doc.save.assert_called_once_with()
