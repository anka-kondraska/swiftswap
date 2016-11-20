"""Models and database functions for Barter Network."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime
import bcrypt
import sys
sys.path.append('..')

db = SQLAlchemy()

#fake app for now, not connected to server.py yet
# app = Flask(__name__)

#######################
# Model definitions and relationships


class User(db.Model):
    """User of Barter Circle"""

    __tablename__ = "users"


    # for networkx and node building 
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_fname = db.Column(db.String(150), nullable=False)
    user_lname = db.Column(db.String(150), nullable=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    # future features
    user_street_address = db.Column(db.String(150), nullable=True)
    user_city = db.Column(db.String(64), nullable=True)
    user_state = db.Column(db.String(2), nullable=True)
    user_zipcode = db.Column(db.String(15), nullable=True)
    user_dob = db.Column(db.DateTime, nullable=True)
    user_occupation = db.Column(db.String(62), nullable=True)
    user_occupation_id = db.Column(db.Integer, nullable=False)

    user_lat = db.Column(db.Float, nullable=True)
    user_lng = db.Column(db.Float, nullable=True)




    # for site log in
    user_email = db.Column(db.String(64), unique=True, nullable=True)
    user_password = db.Column(db.String(500))
    # hashed_pswd = bcrypt.hashpw(password, bcrypt.gensalt())
 





    def __repr__(self):
        """User repr when printed"""

        return "<User user_id=%s user_fname=%s user_email=%s user_password=%s>" % \
                (self.user_id, 
                    self.user_fname, 
                    self.user_email, 
                    self.user_password)

class UserSkill(db.Model): 
    """Users and skills direction of Barter Network"""

    __tablename__ = "userskills"

    userskill_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'), nullable=False)
    skill_direction = db.Column(db.String(4), nullable=False)
    direction_id = db.Column(db.Integer, nullable=False)

    # define relationship to user
    user = db.relationship('User', backref=db.backref('userskills'))

    # define relationship to skill
    # skill = db.relationship('Skill', backref=db.backref('userskills'))



    def __repr__(self):
        """Userskill repr when printed"""
        return "<Userskill userskill_id=%s user_id=%s skill_id=%s skill_direction=%s>" % \
        (self.userskill_id, self.user_id, self.skill_id, self.skill_direction, self.direction_id)


class Skill(db.Model):
    """Skill of Barter Network"""

    __tablename__ = "skills"

    skill_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    skill_name = db.Column(db.String(64), nullable=False)
    skill_value = db.Column(db.Integer, nullable=True) #  for future feature, to use weight attribute for edge, quantify the need for a skill

    def __repr__(self):
        """Skill repr when printed"""

        return "<Skill skill_id=%s skill_name=%s skill_value=%s>" %(self.skill_id, self.skill_name, self.skill_value)



def sample_data():

    user1 = User(user_fname="Anka",user_lname="Kon",
                    user_street_address="683 Sutter Street",user_city="San Francisco",
                    user_state="CA",user_zipcode="94102", user_dob=02-02-1988, 
                    user_occupation="programmer", user_email="anka@anka.com", 
                    user_password="666", user_lat="37.7886679", user_lng="-122.4136874")
    user2 = User(user_fname="Boy",user_lname="George",
                    user_street_address="449 Powell Street",user_city="San Francisco",
                    user_state="CA",user_zipcode="94108", user_dob=01-01-1988, 
                    user_occupation="brick layer", user_email="boy@george.com", 
                    user_password="666", user_lat="37.7888078", user_lng="-122.4111715,")

    skill1 = Skill(skill_name="jogging budy", skill_value=0)
    skill2 = Skill(skill_name="cartooning", skill_value=0)

    userskill1 = UserSkill(user_id=1,skill_id=1,skill_direction="to")
    userskill2 = UserSkill(user_id=1,skill_id=2,skill_direction="from")
    userskill3 = UserSkill(user_id=2,skill_id=1,skill_direction="from")
    userskill4 = UserSkill(user_id=2,skill_id=2,skill_direction="to")

    db.session.add_all([user1, user2, skill1, skill2, userskill1, userskill2, userskill3, userskill4])
    db.session.commit()


################################
# Helper functions

def connect_to_db(app):
    """Connect datatbase to Flask app"""

    # configure PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///barternet'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
     
if __name__ == "__main__":

    from barter_network import app
    # db.create_all()
    connect_to_db(app)
    print "Connected to barternet"
