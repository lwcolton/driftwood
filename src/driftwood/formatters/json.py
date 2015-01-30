import json

from .dict import DictFormatter

class JSONFormatter(DictFormatter):
    """Formats messages as JSON.

    Accepts the same arguments as :class:`~driftwood.formatters.dict.DictFormatter`
    """
    def format(self, record):
        message_dict = super().format(record)
        return json.dumps(message_dict)
