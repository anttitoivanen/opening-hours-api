from flask import Flask, request, make_response, jsonify
from .parser import Parser

app = Flask(__name__)
parser = Parser()

@app.route('/parse_opening', methods=['POST'])
def parse_opening():
	if not request.json:
		resp = make_response(jsonify({'error': 'Missing request body'}), 400)
	try:
		data = parser.validate_input(request.json)
	except ValueError as e:
		resp = make_response(jsonify({'error': str(e)}), 400)
		return resp
	parsed = parser.parse_input(data)
	out = parser.format_output(parsed)
	return out