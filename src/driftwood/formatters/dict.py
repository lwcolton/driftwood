import logging

class DictFormatter(logging.Formatter):
    """Used for formatting log records into a dict."""
    def __init__(self, *args, extra_attrs=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.useful_attrs = ["name","levelno","levelname","pathname","filename","module","lineno",
        "funcName","created","asctime","msecs","relativeCreated","thread","threadName",
        "process"]
        self.useful_attrs += extra_attrs

    def format(self, record):
        message = super().format(record)
        msg_dict = {}
        for attr in self.useful_attrs:
            if hasattr(record, attr):
                msg_dict[attr] = getattr(record, attr)
        msg_dict["message"] = message
        return msg_dict
