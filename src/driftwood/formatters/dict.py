import logging

class DictFormatter(logging.Formatter):
    """Used for formatting log records into a dict.

    .. automethod:: __init__
    """
    def __init__(self, *args, extra_attrs=[], **kwargs):
        """
        :param list extra_attrs: A list of strings specifying additional
            arguments that may exist on the log record instances and
            should be included in the messages.
        """
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
