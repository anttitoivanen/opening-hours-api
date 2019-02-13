WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def pad_zero(num):
	if num < 10:
		return f'0{num}'
	return f'{num}'

def format_time(timestamp):
	hours = timestamp // (60*60)
	minutes = (timestamp // 60) % 60
	seconds = timestamp % 60
	if hours < 12:
		suffix = 'AM'
	else:
		suffix = 'PM'
		hours -= 12
	if hours == 0:
		hours = 12
	if not seconds:
		if not minutes:
			return f'{hours} {suffix}'
		return f'{hours}:{pad_zero(minutes)} {suffix}'
	return f'{hours}:{pad_zero(minutes)}:{pad_zero(seconds)} {suffix}'

def format_range(start, end):
	return f'{start} - {end}'

class Parser:

	def __init__(self):
		pass

	def validate_event(self, event, latest_type):
		# Check attributes and their values for an individual entry in the data
		if not event['type'] or event['type'] not in ['open', 'close']:
			raise ValueError("Event must have either 'open' or 'close' as type")
		if not 0 < int(event['value']) < 86399:
			raise ValueError(f'Timestamp should be in range [0, 86399], got {event["value"]}')
		if event['type'] == latest_type:
			raise ValueError(f"Can not have two '{latest_type}' events in a row")
		return event['type']

	def validate_input(self, data):
		# Make sure the input data matches our expectations
		first_type = None
		latest_type = None
		for day in WEEKDAYS:
			if day not in data:
				raise ValueError(f'No times found for {day}')
			try:
				data[day].sort(key=lambda event: event['value'])
			except KeyError as key:
				raise ValueError(f'Missing key {key} for event on {day}')
			except TypeError:
				raise TypeError('Timestamp must be an integer')
			for event in data[day]:
				latest_type = self.validate_event(event, latest_type)
				if first_type is None:
					first_type = event['type']
		if first_type == latest_type:
			raise ValueError('Can not both start and end the week with an event of the same type')
		return data

	def parse_input(self, data):
		# Parse validated data into the internal format
		current_opening = None
		opening_day = None
		dangling_close = None
		times = {}
		for day in WEEKDAYS:
			times[day] = []
			for event in data[day]:
				if event['type'] == 'open':
					current_opening = format_time(event['value'])
					opening_day = day
				else:
					closing_time = format_time(event['value'])
					if current_opening is not None:
						times[opening_day].append(format_range(current_opening, closing_time))
					else:
						dangling_close = closing_time
		if current_opening and dangling_close:
			times[WEEKDAYS[-1]].append(format_range(current_opening, dangling_close))
		return times

	def format_output(self, data):
		#Prepare parsed data for output
		lines = []
		for day in WEEKDAYS:
			if not data[day]:
				lines.append(f'{day.title()}: Closed')
			else:
				lines.append(f'{day.title()}: {", ".join(data[day])}')
		return '\n'.join(lines)
