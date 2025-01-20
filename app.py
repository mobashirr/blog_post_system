#!/usr/bin/ python3
# Specifies the interpreter to be used for this script (Python 

from application import app
# Imports the 'app' object from the 'application' module


if __name__ == '__main__':
    # Ensures this script is being run directly and not imported as a module
    app.run(debug=True)
    # Starts the Flask application server in debug mode
