import json

from driftwood.formatters.dict import DictFormatter

class JSONFormatter(DictFormatter):
    """Formats messages as JSON.

    This class is a subclass of :py:class:`driftwood.formatters.DictFormatter`,
    and accepts the same arguments for __init__.
    """
    def format(self, record):
        message_dict = super().format(record)
        return json.dumps(message_dict)
