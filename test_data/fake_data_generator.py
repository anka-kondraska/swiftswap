from faker import Faker
from random import choice, sample,randrange
import numpy as np


fake = Faker()

fake.seed(4321)

SKILL = ['gardening','programming','painting','dog walking','brick laying',
         'cooking','cleaning','drawing','carpentry','singing','playing guitar',
         'speak English','speak Spanish','yoga instructor','meditation instructor',
         'play tuba','nails', 'haircut for curly', 'haircut for straight',
         'hairstyling','animal grooming','shopping','driving a car',
         'plumbing','legal form help','bookkeeping','attorney',
         'electronics fixed','tutoring in sciences','tutoring in humanities',
         'dog/cat sitting','party organizing','home organizing',
         'pick up/drop off','laundry','massage','reiki','sewing','baking',
         'moving', 'cleaning rugs','putting up shelves','bread making',
         'pizza making','weaving','leather work','herbalism','acupuncture',
         'dog training','lawn mowing','landscaping','playing piano',
         'composing music','graphic design','cartooning','interior decoration',
         'shoe repair','tailoring','ironing', 'beer making', 'writing poetry',
         'editing', 'tennis instructor', 'soccer instructor','knife skills']


def fake_user():
    
    f = open('test_user.txt', 'w')
    for i in xrange(500):
        f.write(fake.first_name()+'|'+fake.last_name()+'|'+fake.street_address()+
                '|'+fake.city()+'|'+fake.state_abbr()+'|'+fake.zipcode()+
                '|'+fake.date()+'|'+fake.job()+'|'+fake.email()+
                '|'+fake.password(length=6, special_chars=True, 
                    digits=True, upper_case=True, lower_case=True)+'\n')
    f.close()

fake_user()

def fake_skill():
    f = open('test_skill.txt', 'w')
    for i in xrange(65):
        f.write(np.random.choice(SKILL, replace=False)+'|'+'0'+'\n')
    f.close()

fake_skill()




def fake_userskill():
    f = open('test_userskill.txt', 'w')
    for i in xrange(1,501):
        f.write(str(i)+'|'+str(randrange(1,66))+'|'+'to'+'\n')
    for i in xrange(1,501):
        f.write(str(i)+'|'+str(randrange(1,66))+'|'+'from'+'\n')
    f.close()

fake_userskill()


# 1 # 3
# 1 # 3
# 2 # 4
# 3 # 5

