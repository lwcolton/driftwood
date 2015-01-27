import json

from driftwood.formatters.dict import DictFormatter

class JSONFormmater(DictFormatter):
    """Formats messages as JSON"""
    def format(self, record):
        message_dict = super().format(record)
        return json.dumps(message_dict)
