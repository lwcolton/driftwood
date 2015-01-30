import logging
from unittest import mock
import uuid

from driftwood.adapters import StatusUpdateAdapter

class TestStatusAdapter:
    def test_1(self):
        update_func = mock.MagicMock()
        log = logging.getLogger(uuid.uuid4().hex)
        adapter = StatusUpdateAdapter(update_func, log)
        update_func.assert_call_count == 0
        adapter.info("test")
        update_func.assert_called_with(20, "INFO")
        update_func.assert_call_count == 1
        adapter.debug("test")
        update_func.assert_call_count == 1
        adapter.error("test")
        update_func.assert_called_with(40, "ERROR")
        update_func.assert_call_count == 2
        adapter.warning("test")
        adapter.info("test")
        adapter.warning("test")
        update_func.assert_call_count == 2
        

       

