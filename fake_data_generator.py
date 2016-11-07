from faker import Faker


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