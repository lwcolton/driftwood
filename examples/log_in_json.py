import logging
import uuid

from driftwood.formatters import JSONFormatter

log = logging.getLogger("test")
log.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()

formatter = JSONFormatter(extra_attrs = ["loop_num"])

stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)

for loop_num in range(0, 5):
    log.info("doing work", extra={"loop_num":loop_num})
