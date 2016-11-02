"""Barter Network App"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, SkillDirection, UserSkill


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")

@app.route('/register', methods=['GET'])
def barter_up_form():
    """Sign Up form"""

    return render_template("barter_up_form.html")

@app.route('/register', methods=['POST'])
def barter_up_process():
    """Sign Up process"""

    email = request.form.get('email')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    dob = request.form.get('dob')
    occupation = request.form.get('occupation')
    zipcode = request.form.get('zipcode')

    if User.query.filter_by(user_email=email).first():
        flash('Please log in, you are alreday registered')

        redirect('/')
    else:
        new_user = User(user_fname=fname,user_lname=lname,
            user_zipcode=zipcode, user_dob=dob, user_occupation=occupation, 
            user_email=email, user_password=password)
        session['username'] = email

        db.session.add(new_user)

        db.session.commit()

    return render_template("user_profile.html")

@app.route('/logout')
def log_out():

    del session['username']
    flash("logged out!")
    return redirect('/')





####################

if __name__ == "__main__":

    app.debug=True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')