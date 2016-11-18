from faker import Faker, Factory
from random import choice, sample,randrange
import numpy as np
from barnum import gen_data

fake = Factory.create('en_US')

fake.seed(4321)

SKILL = ['gardening','programming','painting','dog walking',
         'cooking','cleaning','drawing','singing','playing guitar',
         'speak English','yoga instructor','meditation instructor','nails','haircut',
         'animal grooming','shopping','driving a car'
         'plumbing','legal form help','bookkeeping',
         'electronics fixed','tutoring',
         'dog/cat sitting','party organizing','home organizing',
         'pick up/drop off','laundry','massage','reiki','sewing','baking',
         'moving','putting up shelves','bread making',
         'pizza making','weaving','leather work','herbalism','acupuncture',
         'dog training','lawn mowing','landscaping','playing piano',
         'composing music','graphic design','cartooning','interior decoration',
         'shoe repair','tailoring','ironing', 'beer making', 'writing poetry',
         'editing', 'tennis instructor', 'soccer instructor','knife skills']


def fake_user():
    f = open('test_user.txt', 'w')
    lat = 40.4365
    lng = -99.3925
    for i in xrange(100):
        lat += 0.0001
        lng -= 0.0001
        zipcode, city, state = gen_data.create_city_state_zip()
        f.write(fake.first_name()+'|'+fake.last_name()+'|'+gen_data.create_street()+
                '|'+city+'|'+state+'|'+zipcode+
                '|'+fake.date()+'|'+gen_data.create_job_title()+'|'+fake.email()+
                '|'+fake.password(length=6, special_chars=True, 
                    digits=True, upper_case=True, lower_case=True)+'|'+str(lat)+'|'+str(lng)+'\n')
    f.close()

fake_user()

def fake_skill():
    f = open('test_skill.txt', 'w')
    # for i in xrange(len(SKILL)):
    for skill in SKILL:
        f.write(skill+'|'+'0'+'\n')
        # f.write(np.random.choice(SKILL, replace=False)+'|'+'0'+'\n')
    f.close()

fake_skill()

def fake_userskill():
    f = open('test_userskill.txt', 'w')
    for i in xrange(1,101):
        f.write(str(i)+'|'+str(randrange(1,len(SKILL)+1))+'|'+'to'+'\n')
    for i in xrange(1,101):
        f.write(str(i)+'|'+str(randrange(1,len(SKILL)+1))+'|'+'from'+'\n')
    f.close()

fake_userskill()




