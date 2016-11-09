"""Barter Network App"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension


from model import connect_to_db, db, User, Skill, UserSkill
import bcrypt
import os

import helper_fun



app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

map_key = os.environ["GOOGLE_API_KEY"]


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
    street_address = request.form.get('street-address')
    city = request.form.get('city')
    state = request.form.get('state')


    if User.query.filter_by(user_email=email).first():
        flash('Please log in, you are alreday registered')

        return redirect('/login')
    else:
        new_user = User(user_fname=fname,user_lname=lname,
            user_zipcode=zipcode,user_street_address=street_address, user_city=city, user_state=state,user_dob=dob, user_occupation=occupation, 
            user_email=email, user_password=bcrypt.hashpw(password.encode('UTF_8'), bcrypt.gensalt()))

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.user_id
        flash('You are now logged in!')
        helper_fun.add_node(new_user.user_id,new_user.user_fname)
    return render_template("user_skill.html", user=new_user)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    return render_template("user_profile.html", user=user,map_key_api = map_key)

@app.route('/simple_cycle.json')
def cycle_data():
    """JSON information about ."""



    # cycles = {
    #     bear.marker_id: {
    #         "bearId": bear.bear_id,
    #         "gender": bear.gender,
    #         "birthYear": bear.birth_year,
    #         "capYear": bear.cap_year,
    #         "capLat": bear.cap_lat,
    #         "capLong": bear.cap_long,
    #         "collared": bear.collared.lower()
    #     }
    #     for cycle in Bear.query.limit(50)}

    return jsonify(cycles)

@app.route('/logout')
def log_out():

    del session['user_id']
    flash("logged out!")
    return redirect('/')

@app.route('/user_skill', methods=['POST'])
def user_skill():

    skill_name_to = request.form.get('skill-name-to')
    skill_name_from = request.form.get('skill-name-from')

    # user_insession = User.query.filter_by(user_email=session['username']).first()
    # user_id_insession = user_insession.user_id

    user_id_insession = session['user_id']

    skillz_to_eval = [(skill_name_to,'to'), (skill_name_from, 'from')]

    # Adding skill to db
    for skill_name, direction in skillz_to_eval:
        skill = db.session.query(Skill.skill_name, Skill.skill_id).join(UserSkill).filter(
                Skill.skill_name==skill_name,
                UserSkill.skill_direction==direction).first()

        if not skill:
            new_skill = Skill(skill_name=skill_name)
            db.session.add(new_skill)
            db.session.commit()
            skill = new_skill

        new_userskill = UserSkill(user_id=user_id_insession, 
                                  skill_id=skill.skill_id, skill_direction=direction)
        db.session.add(new_userskill)
        db.session.commit()
        flash("your skills have been added to our network")
    return redirect('/')

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(user_email=email).first()

    if not user:
        flash("No such user")
        return redirect("/register")

    if bcrypt.hashpw(password.encode('UTF_8'), user.user_password.encode('UTF_8')).decode() == user.user_password:
        flash("it Matches")
    else:
        flash("Incorrect password")
         

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)







####################

if __name__ == "__main__":

    app.debug=True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')