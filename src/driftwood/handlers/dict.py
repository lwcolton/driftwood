import logging

from driftwood.formatters.dict import DictFormatter

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
        """emits things"""
        return self._dict_formatter.format(record)
