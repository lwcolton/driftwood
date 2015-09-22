import json

from .json import JSONFormatter

class SplunkFormatter(JSONFormatter):
    """Formats messages as JSON with order preserved for splunk

    Accepts the same arguments as :class:`~driftwood.formatters.json.JSONFormatter`
    """
    def __init__(self, *args, **kwargs):
        kwargs.set_default("preserve_order", True)
        kwargs.set_default("specific_order", ["created"])
        kwargs.set_default("regular_attrs", 
            [
                "created", "levelname", "message", "pathname",
                "lineno", "funcName", "process", "levelno"
            ]
        )
        super().__init__(*args, **kwargs)
