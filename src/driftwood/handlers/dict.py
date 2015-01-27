import logging

from driftwood.formatters.dict import DictFormatter

class DictHandler(logging.Handler):
    """Formats log records into a dict.

    Meant to be subclassed.  
    This is just a convenience wrapper around `~driftwood.formatters.dict.DictFormatter`.
    """
    def __init__(self, *args, extra_attrs=[], **kwargs):
        """
        Args:
            extra_attrs (list): String names of extra attributes that may exist on the log record.
        """
        super().__init__(*args, **kwargs)
        self._dict_formatter = DictFormatter(extra_attrs=extra_attrs)

    def emit(self, record):
        """Super this in your subclass to format the record into a dict"""
        return self._dict_formatter.format(record)
