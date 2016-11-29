from flask_debugtoolbar import DebugToolbarExtension
from barter_network import app

# running flask server
app.run(host='0.0.0.0', debug=True)
DebugToolbarExtension(app)