import logging
import random
import mock
import uuid

regular_attrs = ["name","levelno","levelname","pathname","filename","module","lineno",
    "funcName","created","msecs","relativeCreated","thread","threadName",
    "process"]

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
