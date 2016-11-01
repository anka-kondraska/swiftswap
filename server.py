"""Barter Network App"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash, session, url_for)
from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy.orm import joinedload

from model import (connect_to_db, db, User, Skill, Userskill)


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("templates/homepage.html")





####################
if __name__ == "__main__":
    app.debug=True
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000)