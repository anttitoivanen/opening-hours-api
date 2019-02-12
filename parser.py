import json, sys

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
	parts = [hours]
	if not seconds:
		if not minutes:
			return f'{hours} {suffix}'
		return f'{hours}:{pad_zero(minutes)} {suffix}'
	return f'{hours}:{pad_zero(minutes)}:{pad_zero(seconds)} {suffix}'

def format_range(start, end):
	return f'{start} - {end}'

def parse_input(data):
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

def validate_input(data):
	first_type = None
	latest_type = None
	for day in WEEKDAYS:
		if day not in data:
			raise ValueError(f'No times found for {day}')
		try:
			data[day].sort(key=lambda event: event['value'])
			for event in data[day]:
				if first_type is None:
					first_type = event['type']
				if not 0 < event['value'] < 86399:
					raise ValueError(f'Timestamp should be in range [0, 86399], got {timestamp}.')
				if event['type'] == latest_type:
					raise ValueError(f'Can not have two {latest_event} events in a row on {day}.')
				latest_type = event['type']
		except KeyError as key:
			raise ValueError(f'Missing key {key} for event on {day}')
	if first_type == latest_type:
		raise ValueError(f'Can not both start and end the week with an event of the same type')
	return data

if __name__ == '__main__':
	data = {"monday" : [{"type": "close", "value": 1200}],"tuesday" : [{"type" : "open","value" : 36000},{"type" : "close","value" : 64800}],"wednesday" : [],"thursday" : [{"type" : "open","value" : 36000},{"type" : "close","value" : 64800}],"friday" : [{"type" : "open","value" : 36000}],"saturday" : [{"type" : "close","value" : 3600},{"type" : "open","value" : 36000}],"sunday" : [{"type" : "close","value" : 3600},{"type" : "open","value" : 43200},{"type" : "close","value" : 75600}, {"type": "open", "value": 84600}]}
	validated = validate_input(data)
	parsed = parse_input(validated)
	print(parsed)