# Driftwood #
**A collection of python logging extensions**

## Features ##
- Compatible with Python 3
- Provides Dictionary, JSON, and MongoDB logging
- Features for logging custom attributes
- Can notify of status changes based on the level of messages being logged

## Installing ##
```shell
git clone https://github.com/HurricaneLabs/driftwood.git
cd driftwood
pip install file://`pwd`
```
**Note:** To use mongodb logging, you must install the mongoengine module.  Tested with 0.8.7

## Examples ##

### JSON Formatter ###
This is a great way to easily log in a machine-parsable format.
While the example uses a StreamHandler for brevity, the most common
production implementation is using a a RotatingFileHandler.
```python
import logging
from driftwood.formatters.json import JSONFormatter
log = logging.getLogger("test")
handler = logging.StreamHandler()
json_formatter = JSONFormatter()
handler.setFormatter(json_formatter)
log.addHandler(handler)
log.warning("uh oh")
```
Output:
```json
{"created": 1422386241.4394472, "pathname": "<stdin>", "message": "uh oh", "threadName": "MainThread", "levelname": "WARNING", "process": 4384, "module": "<stdin>", "thread": 139785634490176, "levelno": 30, "msecs": 439.44716453552246, "filename": "<stdin>", "lineno": 1, "relativeCreated": 52455.650329589844, "funcName": "<module>", "name": "test"}
```
