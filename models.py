from dataclasses import dataclass
from datetime import date
from carpool import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class DB_handler(): #hanterar det som ska skickas till och från databasen, om vi skulle ha det i t.ex car_manager skulle den bli för stor.
	__init__(self): # Tror inte vi ska ha någon sådan klass
	

@dataclass
class User(db.Model):
	id: int
	username: str
	email: str
	image: str
	password: str
	std_destination: str
		
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	email = db.Column(db.String(130), unique=True, nullable=False)
	image = db.Coulm(db.String(30), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	std_destination = db.Column(db.String(30))

	def __repr__(self):
	    return f"User('{self.username}', '{self.email}', '{self.image}')"


@dataclass
class Car(db.Model):
	id : int
	car_name: str
	model: str
	license_plate: str
	fuel: str
	seats: str
	user_id: int
	user: User

	id = db.Column(db.Integer, primary_key=True)
	car_name = db.Column(db.String(30), unique=True, nullable=False)
	model = db.Column(db.String(20, nullable=False))
	license_plate = db.Column(db.String(10), unique=True, nullable=False)
	fuel = db.Column(db.String(20), nullable=False)
	seats = db.Column(db.Integer, nullable=False)
	booked = db.Column(db.Boolean, nullable=False, default==False)
	user_name = db.Column(db.String(30), db.ForeignKey('user.name'))
	user = relaitionship(User)
	
	def __repr__(self):
        	return f"Car('{self.name}', '{self.owner}')"


@dataclass
class CarManager(db.Model):
	id: int
	days: list
	car: Car 
	user: User
	money_spent: int
	milage: int
    
	id = db.Column(db.Integer, primary_key=True
	day = db.Column(db.datetime.date(), default = date.now())
	car_id = db.Column(db.String, db.ForeignKey('car.license_plate')nullable = False)
	car = relationship(Car) 
	user_id = db.relationship(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = relationship(User)
	money_spent = db.Column(db.Integer, db.ForeignKey(User), default=0)
	milage = db.Column(db.Integer, ForeignKey(User), default=0)
        
    
@dataclass
class Token(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_expired = db.Column(db.DateTime, nullale=False)
	token = db.Column(db.String(60), nullable=False, index=True)
	
