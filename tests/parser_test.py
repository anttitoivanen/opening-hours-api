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
		self.validdata = {
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

	def test_valid_data(self):
		parsed = self.parser.parse_input(self.validdata)
		self.assertEqual(parsed['monday'], [])


if __name__ == '__main__':
	unittest.main()