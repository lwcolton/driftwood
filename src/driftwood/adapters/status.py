import logging

class StatusUpdateAdapter(logging.LoggerAdapter):
    """Used to notify a callback about changes in the loglevel of a program.

    Will call a callback function when a program logs a message of 
    increasing severity.
    """
    def __init__(self, status_update_func, *args, **kwargs):
        """
        Args:
            status_update_func (callable): Called when the status changes.
        """
        super().__init__(*args, **kwargs)
        self.status_num = 0
        self.status_update_func = status_update_func

    def log(self, *args, **kwargs):
        super().log(*args, **kwargs)
        level = args[0]
        if level > self.status_num:
            self.status_num = level
            self.status_update_func(level)
