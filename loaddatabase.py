import os
from datetime import date
from carpool import db, bcrypt
from carpool.models import User, Car, CarManager


try:
    os.remove('carpool/site.db')
    print('previous DB file removed')
except:
    print('no previous file found')

db.create_all()

hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')

default_user_1 = User(username='Anna',
                      email='anna@test.com',
                      password=hashed_password)
db.session.add(default_user_1)

default_user_2 = User(username='Bengt',
                      email='bengt@test.com',
                      password=hashed_password)
db.session.add(default_user_2)


default_user_3 = User(username='Carl',
                      email='carl@test.com',
                      password=hashed_password)
db.session.add(default_user_3)


default_car_1 = Car(car_name ='Lightning McQueen',
                   model = 'sedan',
                   license_plate = 'AAA000',
                   fuel = 'gas',
                   seats = 5)
                   #user=default_user1,
                   #user_name = user.username)
db.session.add(default_car_1)


default_car_2 = Car(car_name ='Testarossa',
                   model = 'coupe',
                   license_plate = 'RRR333',
                   fuel = 'gas',
                   seats = 2)
                    #user=default_user1, user_name = user.username)
db.session.add(default_car_2)


default_car_3 = Car(car_name ='i3',
                   model = 'combi',
                   license_plate = 'BMW123',
                   fuel = 'electric',
                   seats = 4)
                  #booked = False, user=default_user1, user_name = user.username)
db.session.add(default_car_3)


booking_1 = CarManager(day = date(20-03-20),
                       car = default_car_1,
                       car_id = default_car_1.id,
                       user = default_user_1,
                       user_id = default_user_1.id)
db.session.add(booking_1)


booking_2 = CarManager(day = date(20-04-20),
                       car = default_car_2,
                       car_id = default_car_2.id,
                       user = default_user_2,
                       user_id = default_user_2.id)
db.session.add(booking_2)


booking_3 = CarManager(day = date(20-05-01),
                       car = default_car_1,
                       car_id = default_car_1.id,
                       user = default_user_3,
                       user_id = default_user_3.id)

db.session.commit()

print('finalized')
