from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, number_range
from flaskblog.models import User, Car, CarManager
from datetime import date



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    std_destination = StringField('Standard Destination',
                                  validators = [DataRequired(), Length(min=1, max=50)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class UpdateCar(FlaskForm):
    car_name = StringField('Car name', validators=[DataRequired(), Length(min=1, max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(min=1, max=50)])
    license_plate = StringField('License plate', validators=[DataRequired(), Length(min=4, max=10)])
    fuel = IntegerField('Current fuel percentage (must be a number)', validators=[DataRequired(), number_range(0, 100)])
    seats = IntegerField('Number of seats (must be a number)', validators=[DataRequired()])
    info = TextAreaField('Additional info')
    picture = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update car')



class AddCarForm(FlaskForm):
    car_name = StringField('Car name', validators=[DataRequired(), Length(min=1, max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(min=1, max=50)])
    license_plate = StringField('License plate', validators=[DataRequired(), Length(min=4, max=10)])
    fuel = IntegerField('Current fuel percentage (must be a number)', validators=[DataRequired(), number_range(0,100)])
    seats = IntegerField('Number of seats (must be a number)', validators=[DataRequired()])
    info = TextAreaField('Additional info')
    picture = FileField('Add picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add car')

    def validate_license_plate(self, license_plate):
        car = Car.query.filter_by(license_plate=license_plate.data).first()
        if car:
            raise ValidationError('Car license plate already registered.')



class NewBooking(FlaskForm):
    day = DateField('Choose a date you would like to book a car', format='%Y-%m-%d')
    destination = StringField('Choose your destination', validators=[DataRequired()])
    submit = SubmitField('Confirm booking')
    combo = StringField('combo')
    update =BooleanField('update')

    def validate_day(self, day):
        update = self.update.data
        combo = self.combo.data
        if isinstance(day.data, date):
            if day.data < date.today():
                raise ValidationError('Date has already passed, please choose another.')

        if CarManager.query.filter_by(combination=f'{combo}').first() and not update:
            raise ValidationError('Car is already booked this date, please choose another date.')



class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send comment')
