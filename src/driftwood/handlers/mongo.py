import logging

import mongoengine

from driftwood.handlers.dict import DictHandler

class BaseLogRecord(mongoengine.Document):
    meta = {'allow_inheritance': True, 'abstract': True}
    msecs = mongoengine.FloatField()
    name = mongoengine.StringField(required=True)
    levelname = mongoengine.StringField()
    pathname = mongoengine.StringField()
    process = mongoengine.IntField()
    lineno = mongoengine.IntField()
    relativeCreated = mongoengine.FloatField()
    funcName = mongoengine.StringField()
    created = mongoengine.FloatField()
    message = mongoengine.StringField(required=True)
    threadName = mongoengine.StringField()
    filename = mongoengine.StringField()
    levelno = mongoengine.IntField()
    thread = mongoengine.LongField()
    module = mongoengine.StringField()

class LogRecord(BaseLogRecord):
    pass

class MongoHandler(DictHandler):
    def __init__(self, *args, document=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not document:
            raise AttributeError("document is required")
        if document == None:
            document = LogRecord
        self.document = document

    def emit(self, record):
        msg_dict = super().emit(record)
        log_doc = self.document()
        for msg_key, msg_value in msg_dict.items():
            setattr(log_doc, msg_key, msg_value)
        log_doc.save()
