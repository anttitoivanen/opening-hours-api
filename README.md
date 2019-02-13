# Opening hours API

Parse restaurant opening hour data from json into a human-readable plaintext format

## Setup

1. Clone this repository and navigate to the newly created directory
2. Set up a new virtual environment, e.g. `python3 -m venv .venv`
3. Activate the environment: `source .venv/bin/activate`
4. Install reuirements: `pip install -r requirements.txt`

## Running

The project is built with flask, and can be run with e.g. `FLASK_APP=src/api.py flask run` in the root directory. The service then accepts HTTP POST requests at http://localhost:5000/parse_opening

## Testing

This project uses nosetests for testing. To run all tests, use the command `nosetests` in the project root.