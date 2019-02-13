from flask import Flask, request, make_response, jsonify
from .parser import Parser

app = Flask(__name__)
parser = Parser()

@app.route('/parse_opening', methods=['POST'])
def parse_opening():
	if not request.data or not request.json:
		return make_response('Error: Missing or empty request body', 400)
	try:
		data = parser.validate_input(request.json)
	except ValueError as e:
		return make_response(f'Error: {str(e)}', 400)
	parsed = parser.parse_input(data)
	out = parser.format_output(parsed)
	return out