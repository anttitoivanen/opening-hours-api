import unittest
from src import format_time, Parser

class TestTime(unittest.TestCase):

	def setUp(self):
		pass

	def test_valid_time_formats(self):
		self.assertEqual(format_time(0), '12 AM')
		self.assertEqual(format_time(32400), '9 AM')
		self.assertEqual(format_time(37800), '10:30 AM')
		self.assertEqual(format_time(86399), '11:59:59 PM')

class TestParser(unittest.TestCase):

	def setUp(self):
		self.parser = Parser()

	def test_mising_key(self):
		missing_weekday = {
		"monday": [],
		}
		with self.assertRaisesRegexp(ValueError, 'No times found for tuesday') as err:
			self.parser.validate_input(missing_weekday)

	def tet_invalid_times(self):
		wrong_type = {
			"monday" : [],
			"tuesday" : [
				{"type" : "open","value" : 36000},
				{"type" : "close"}
			],
			"wednesday" : [],
			"thursday" : [],
			"friday" : [],
			"saturday" : [],
			"sunday" : []
		}
		expected_error = "Missing key 'value' for event on tuesday"
		with self.assertRaisesRegexp(ValueError, expected_error) as err:
			self.parser.validate_input(wrong_type)
		wrong_type['tuesday'][-1]['value'] = "asd"
		expected_error = "Timestamp must be an integer"
		with self.assertRaisesRegexp(TypeError, expected_error):
			self.parser.validate_input(wrong_type)
		wrong_type['tuesday'][-1]['value'] = -1
		expected_error = "Timestamp should be in range \[0, 86399\], got -1"
		with self.assertRaisesRegexp(ValueError, expected_error):
			self.parser.validate_input(wrong_type)

	def test_event_order(self):
		events = {
			"monday": [
				{'type': 'open', 'value': 1200},
				{'type': 'close', 'value': 12000},
				{'type': 'close', 'value': 13000}
			],
			"tuesday" : [],
			"wednesday" : [],
			"thursday" : [],
			"friday" : [],
			"saturday" : [],
			"sunday" : []
		}
		expected_error = "Can not have two 'close' events in a row"
		with self.assertRaisesRegexp(ValueError, expected_error):
			self.parser.validate_input(events)
		events['monday'].append({'type': 'open', 'value': 12500})
		events['tuesday'].append({'type': 'open', 'value': 4600})
		expected_error = "Can not both start and end the week with an event of the same type"
		with self.assertRaisesRegexp(ValueError, expected_error):
			self.parser.validate_input(events)

	def test_valid_data(self):
		# data from the assignment
		validdata = {
			"monday" : [],
			"tuesday" : [
				{"type" : "open","value" : 36000},
				{"type" : "close","value" : 64800}
			],
			"wednesday" : [],
			"thursday" : [
				{"type" : "open","value" : 36000},
				{"type" : "close","value" : 64800}
			],
			"friday" : [
				{"type" : "open","value" : 36000}
			],
			"saturday" : [
				{"type" : "close","value" : 3600},
				{"type" : "open","value" : 36000}
			],"sunday" : [
				{"type" : "close","value" : 3600},
				{"type" : "open","value" : 43200},
				{"type" : "close","value" : 75600}
			]
		}
		parsed = self.parser.parse_input(validdata)
		self.assertEqual(parsed['monday'], [])
		self.assertEqual(parsed['tuesday'], ['10 AM - 6 PM'])
		self.assertEqual(parsed['wednesday'], [])
		self.assertEqual(parsed['thursday'], ['10 AM - 6 PM'])
		self.assertEqual(parsed['friday'], ['10 AM - 1 AM'])
		self.assertEqual(parsed['saturday'], ['10 AM - 1 AM'])
		self.assertEqual(parsed['sunday'], ['12 PM - 9 PM'])

		# what happes when sunday overflows to monday
		validdata['monday'] = [{
			'type': 'close',
			'value': 3600
		}]
		validdata['sunday'].append({
			'type': 'open',
			'value': 79200
		})
		overflowing = self.parser.parse_input(validdata)
		self.assertEqual(overflowing['sunday'], ['12 PM - 9 PM', '10 PM - 1 AM'])


if __name__ == '__main__':
	unittest.main()