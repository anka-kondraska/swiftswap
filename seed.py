"""Seed the test database with test data"""



from sqlalchemy import func
from model import User, UserSkill, SkillDirection

from model import connect_to_db, db
from server import app



def load_users():
    """"""

    print "Users"

    for row in open("test_data/test_user.txt"):
        row = row.rstrip()
        # row=row.split("|")
        # print row
        u_id, fname, lname, street_address, city, state, zipcode, date, occupation, email, password = row.split("|")
                    

        user = User(user_id=u_id,user_fname=fname,user_lname=lname,
                    user_street_address=street_address,user_city=city,
                    user_state=state,user_zipcode=zipcode, user_dob=date, user_occupation=occupation, user_email=email, user_password=password)


        db.session.add(user)
    db.session.commit()

def load_userskills():
    """"""

    print "Userskills"
    
    for row in open("test_data/test_userskill.txt"):
        row = row.rstrip()
        us_id, u_id, s_id = row.split("|")
                    

        userskill = UserSkill(userskill_id=us_id,user_id=u_id,skill_id=s_id)# skill_direction=direction
                    

        db.session.add(userskill)
    db.session.commit()

def load_skills():
    """"""

    print "Skills"
    
    for row in open("test_data/test_skill.txt"):
        row = row.rstrip()
        s_id, name, value, direction = row.split("|")
                    

        skill = SkillDirection(skill_id=s_id,skill_name=name,skill_value=value, skill_direction=direction)
                    

        db.session.add(skill)
    db.session.commit()


#############################
def set_val_user_id():

    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id+1})
    db.session.commit()

def set_val_skill_id():

    result_skill = db.session.query(func.max(Skill.skill_id)).one()
    max_id_skill = int(result_skill[0])

    query_skill = "SELECT setval('skills_skill_id_seq', :new_id_skill)"
    db.session.execute(query_skill, {'new_id_skill': max_id_skill+1})
    db.session.commit()

if __name__ == "__main__":

    
    connect_to_db(app)
    db.drop_all()
    db.create_all()

    load_users()
    load_skills()
    load_userskills()
    
    set_val_user_id()
    set_val_skill_id()



