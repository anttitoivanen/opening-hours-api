# Opening hours API

Parse restaurant opening hour data from json into a human-readable plaintext format

## Setup

1. Clone this repository and navigate to the newly created directory
2. Set up a new virtual environment, e.g. `python3 -m venv .venv`
3. Activate the environment: `source .venv/bin/activate`
4. Install reuirements: `pip install -r requirements.txt`

## Running

The project is built with flask, and can be run with e.g. `FLASK_APP=src/api.py flask run` in the root directory. The service then accepts HTTP POST requests at http://localhost:5000/parse_opening and returns the formatted output as an HTTP response.

## Testing

This project uses nosetests for testing. To run all tests, use the command `nosetests` in the project root.


## My thoughts on the exercise

On a first note, I think the structure of the exercise was well thought out in the sense that there was the little algorithmic chllenge of parsing the data, coupled with the software engineering perspective of how to structure a project and and build an API.

The format of the data is probably adequate for the purposes discussed here, but I'm not certain that splitting the opening and closing times into named objects per weekday brings much additional benefit. It certainly improves human-readability, which is nevertheless probably not the top priority of the format, at the cost of making parsing it a bit more troublesome. Listing all timestamps as seconds since 12 AM on Monday might make it slightly easier to work with opening hours which may span several weekdays anyway.

For a more realistic use case there are obviously a lot of complexities this format is not designed to handle (timezones, daylight savings, special opening hours for holidays etc.)