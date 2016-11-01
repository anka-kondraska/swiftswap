"""Seed the test database with test data"""



from sqlalchemy import func
from model import User, Userskill, Skill

from model import connect_to_db, db
from server import app



def load_users():
    """"""

    print "Users"

    for row in open("test_data/test_user.txt"):
        row = row.rstrip()
        # row=row.split("|")
        # print row
        u_id, fname, lname, street_address, city, state, zipcode, age, occupation, email, password = row.split("|")
                    

        user = User(user_id=u_id,user_fname=fname,user_lname=lname,
                    user_street_address=street_address,user_city=city,
                    user_state=state,user_zipcode=zipcode, user_age=age, user_occupation=occupation, user_email=email, user_password=password)


        db.session.add(user)
    db.session.commit()

def load_userskills():
    """"""

    print "Userskills"
    
    for row in open("test_data/test_userskill.txt"):
        row = row.rstrip()
        us_id, u_id, s_id, direction = row.split("|")
                    

        userskill = UserSkill(userskill_id=us_id,user_id=u_id,skill_id=s_id,
                    skill_direction=direction)
                    

        db.session.add(userskill)
    db.session.commit()

def load_skills():
    """"""

    print "Skills"
    
    for row in open("test_data/test_skill.txt"):
        row = row.rstrip()
        s_id, name, value = row.split("|")
                    

        skill = Skill(skill_id=s_id,skill_name=name, skill_value=value)
                    

        db.session.add(skill)
    db.session.commit()


#############################
def set_val_user_id():

    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id+1})
    db.session.commit()

if __name__ == "__main__":

    
    connect_to_db(app)
    db.drop_all()
    db.create_all()

    load_users()
    load_skills()
    load_userskills()
    
    set_val_user_id()



