from flask import Flask, request, make_response
from .parser import Parser

app = Flask(__name__)
parser = Parser()

# Set up a default class for responses that always has the type text/plain
# We want to be consistent ith response types, but not to set them every time
class PlainTextResponse(app.response_class):
	def __init__(self, *args, **kwargs):
		super(PlainTextResponse, self).__init__(*args, **kwargs)
		self.mimetype = 'text/plain'
app.response_class = PlainTextResponse

@app.route('/parse_opening', methods=['POST'])
def parse_opening():
	if not request.data or not request.json:
		message = 'Error: Missing or empty request body'
		return make_response(message, 400)
	try:
		data = parser.validate_input(request.json)
	except ValueError as e:
		message = f'Error: {e}'
		return make_response(message , 400)
	parsed = parser.parse_input(data)
	result = parser.format_output(parsed)
	return make_response(result, 200)

@app.errorhandler(400)
def bad_request(error):
	return make_response('Bad request', 400)

@app.errorhandler(405)
def method_not_alowed(error):
	return make_response('Method not allowed', 405)

@app.errorhandler(500)
def internal_error(error):
	return make_response('There was in internal error', 500)