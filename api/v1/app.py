#!/usr/bin/python3
"""API routes and functionality here"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

# Register blueprint
app.register_blueprint(app_views)


# app context
@app.teardown_appcontext
def teardown_context(exception):
    storage.close()


if __name__ == "__main__":
    # Configure host and Port
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))

# Run the Flask server
    app.run(host=host, port=port, treaded=True)
