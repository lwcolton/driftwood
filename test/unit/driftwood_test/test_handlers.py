import json
import logging
import random
from unittest import mock
import uuid

from nose2.tools import params

from driftwood.handlers.dict import DictHandler
from driftwood.handlers.mongo import MongoHandler
from driftwood_test import util

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
        print(mock_doc)
        mock_doc = mock.MagicMock()
        with mock.patch("driftwood.handlers.mongo.LogRecord") as mock_LogRecord:
            mock_LogRecord.return_value = mock_doc
            handler = MongoHandler()
        log = logging.getLogger(uuid.uuid4().hex)
        print (handler.document)
        if not log.hasHandlers():
            log.addHandler(handler)
        
        
        
