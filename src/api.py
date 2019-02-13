from flask import Flask, request, make_response, jsonify
from .parser import Parser

app = Flask(__name__)
parser = Parser()

response_headers = {'Content-Type': 'text/plain'}

@app.route('/parse_opening', methods=['POST'])
def parse_opening():
	if not request.data or not request.json:
		message = 'Error: Missing or empty request body'
		return make_response(message, 400, response_headers)
	try:
		data = parser.validate_input(request.json)
	except ValueError as e:
		message = f'Error: {str(e)}'
		return make_response(message , 400, response_headers)
	parsed = parser.parse_input(data)
	result = parser.format_output(parsed)
	return make_response(result, 200, response_headers)