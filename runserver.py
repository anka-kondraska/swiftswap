#!/usr/bin/python

from barter_network import app
from flask_debugtoolbar import DebugToolbarExtension


DebugToolbarExtension(app)
app.run(host='0.0.0.0', debug=True)

