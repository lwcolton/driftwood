import logging

from driftwood.formatters import DictFormatter

class DictHandler(logging.Handler):
    """Formats log records into a dict.

    Meant to be subclassed.

    Args:
        extra_attrs (list): String names of extra attributes that may exist on the log record.
    """
    def __init__(self, *args, extra_attrs=[], **kwargs):
        super().__init__(*args, **kwargs)
        self._dict_formatter = DictFormatter(extra_attrs=extra_attrs)

    def emit(self, record):
        return self._dict_formatter.format(record)
