import logging

class StatusUpdateAdapter(logging.LoggerAdapter):
    def __init__(self, status_update_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_num = 0
        self.status_update_func = status_update_func

    def log(self, *args, **kwargs):
        super().log(*args, **kwargs)
        level = args[0]
        if level > self.status_num:
            self.status_num = level
            self.status_update_func(level)