import logging

import mongoengine

from driftwood.handlers.dict import DictHandler

class BaseLogRecord(mongoengine.Document):
    meta = {'allow_inheritance': True, 'abstract': True}
    msecs = meng.FloatField()
    name = meng.StringField(required=True)
    levelname = meng.StringField()
    pathname = meng.StringField()
    process = meng.IntField()
    lineno = meng.IntField()
    relativeCreated = meng.FloatField()
    funcName = meng.StringField()
    created = meng.FloatField()
    message = meng.StringField(required=True)
    threadName = meng.StringField()
    filename = meng.StringField()
    levelno = meng.IntField()
    thread = meng.LongField()
    module = meng.StringField()

class GenericLogRecord(BaseLogRecord):
    pass

class MongoHandler(DictHandler):
    def __init__(self, *args, document=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not document:
            raise AttributeError("document is required")
        if document == None:
            document = GenericLogRecord
        self.document = document

    def emit(self, record):
        msg_dict = super().emit(record)
        log_doc = self.document()
        for msg_key, msg_value in msg_dict.items():
            setattr(log_doc, msg_key, msg_value)
        log_doc.save()
