import os
from datetime import date
from carpool import db, bcrypt
from carpool.models import User, Car, CarManager


### Ändra nedan ###
try:
    os.remove('flaskblog/site.db')
    print('previous DB file removed')
except:
    print('no previous file found')

db.create_all()

hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
default_user = User(username='Default', email='default@test.com', image = default.jpg, money_spent = 0, mileage = 0, 
                    password=hashed_password)

db.session.add(default_user)

default_car = Car(car_name ='Lightning McQueen', car_type = 'sedan', liscence_plate = 'AAA000', fuel = 'gas', seats = 5  
                  booked = False, user=default_user, user_name = user.username)

db.session.add(car)

booking = Booking(day = date.now(), car = default_car, car_id = car.id = user = default_user, user_id = user.id)

db.session.add(booking)

db.session.commit()

print('finalized')
