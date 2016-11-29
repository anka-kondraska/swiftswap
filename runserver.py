from flask_debugtoolbar import DebugToolbarExtension
from barter_network import app

app.run(host='0.0.0.0', debug=True)
DebugToolbarExtension(app)