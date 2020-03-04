from dataclasses import dataclass
from datetime import date
from flaskblog import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@dataclass
class User(db.Model):
    id: int
    username: str
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(130), unique=True, nullable=False)
    image = db.Coulm(db.String(30), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nulable=False)
    cars = db.relationship('Car', backref='car_owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"


#@dataclass
#class CarOwner(User, db.Model):
#    car = db.relationship('Car', backref='owner', lazy=True)

    
@dataclass
class CarManager(db.Model):
    car: Car
    days: list
    user: User
    
    day = db.Column(db.datetime.date(), default = date.now())
    car = db.Column(db.String, db.ForeignKey('car.license_plate')nullable = False)
    car = relationship('Car')
        
    
@dataclass
class Car(db.Model):
    id : int
    car_name: str
    type: str
    license_plate: str
    fuel: str
    seats: str
    #owner: CarOwner
    booked: boolean
    user: User

    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(30), unique=True, nullable=False)
    #owner = relationship(CarOwner)
    type = db.Column(db.String(20, nullable=False))
    license_plate = db.Column(db.String(10), unique=True, nullable=False)
    fuel = db.Column(db.String(20), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    booked = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(30), db.ForeignKey('user.name'), nullable=False)
    user = relaitionship(User)


    def __repr__(self):
        return f"Car('{self.name}', '{self.owner}')"


@dataclass
class Token(db.Model)
    id = db.Column(db.Integer, primary_key=True)
    date_expired = db.Column(db.DateTime, nullale=False)
    token = db.Column(db.String(60), nullable=False, index=True)
