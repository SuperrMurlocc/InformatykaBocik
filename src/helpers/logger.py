import json
import logging
import os
from collections import OrderedDict
from datetime import date

LOG_PATH = 'log/'

py_to_JSON = OrderedDict([
    ("'", '"'),
    ("False", 'false'),
    ("True", 'true'),
    ("None", 'null')
])


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def configure_logging():
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
        print(f"Created {LOG_PATH} directory")

    sessionID = date.today().strftime("%d-%m-%Y-") + str(os.getpid()) + '.json'

    name = LOG_PATH + 'log-' + sessionID
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logger.addFilter(NoParsingFilter())
    handler = logging.FileHandler(filename=name, encoding='utf-8', mode='w')
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)


class NoParsingFilter(logging.Filter):
    # TODO: Fix this filter to only display relevant messages
    def filter(self, record):
        return 'WebSocket Event' in record.getMessage() or record.getMessage().startswith('POST')


class JSONFormatter(logging.Formatter):
    def __init__(self):
        pass  # override logging.Formatter constructor

    def format(self, record):
        message = record.getMessage()
        message = message[message.find('{'):]
        message = replace_all(message, py_to_JSON)

        event = {}
        if message.endswith('}'):
            event = json.loads(message)

        event_data = getattr(record, "event_data", None)
        if event_data:
            event.update(event_data)
        if record.exc_info:
            event["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            event["stack_info"] = self.formatStack(record.stack_info)
        if message.endswith('}'):
            return json.dumps(event)
        return ''
