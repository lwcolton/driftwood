import logging

from driftwood.formatters import DictFormatter

class DictHandler(logging.Handler):
    def __init__(self, *args, extra_attrs=[], **kwargs):
        super().__init__(*args, **kwargs)
        self._dict_formatter = DictFormatter(extra_attrs=extra_attrs)
