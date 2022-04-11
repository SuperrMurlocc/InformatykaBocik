import json
import logging
from collections import OrderedDict

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