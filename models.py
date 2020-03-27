from dataclasses import dataclass
from datetime import datetime, date
from flaskblog import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@dataclass
class User(db.Model, UserMixin):
    id: int
    username: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    std_destination = db.Column(db.String(30), nullable=False, default='Gothenburg')
    cars = db.relationship('Car', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@dataclass
class Car(db.Model):
    id: int
    car_name: str
    model: str
    license_plate: str
    fuel: str
    seats: str
    user_id: int
    user: User

    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(30), unique=False, nullable=False)
    model = db.Column(db.String(20), nullable=False)
    license_plate = db.Column(db.String(10), unique=True, nullable=False)
    fuel = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    user = relationship(User)
    user_id = db.Column(db.String(20), db.ForeignKey('user.id'), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default_car.jpg')
    info = db.Column(db.String(300))
    comments = db.relationship('Comment2', backref='comm', lazy=True, order_by='desc(Comment2.date_posted)')

    def __repr__(self):
        return f"Car('{self.car_name}')"



@dataclass # using dataclass you don't need to have the serialize function
class Post(db.Model):
    # but you need to identify the types of the fields
    id: int
    title: str
    content: str
    content_type: str
    user: User

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    # loading comments in the reverse order of date_posted
    comments = db.relationship('Comment', backref='comm', lazy=True, order_by='desc(Comment.date_posted)')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    # but with the serialize() allows you to get information from relationships
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'content_type': self.content_type,
            'user': self.user_id,
            'username': self.user.username
        }


@dataclass
class Comment(db.Model):
    id: int
    content: str
    user: User

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = relationship(Post)

@dataclass
class Comment2(db.Model):
    id: int
    content: str
    user: User

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    car = relationship(Car)



@dataclass
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_expired = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(60), nullable=False, index=True) # index helps searching


@dataclass
class CarManager(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False, default=date.today())
    car = relationship(Car)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    destination = db.Column(db.String(30), nullable=False)


    def __repr__(self):
        return f"Car('{self.day}')"







