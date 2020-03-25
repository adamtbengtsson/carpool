import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from carpool import app, db, bcrypt
from carpool.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm, BookForm
from carpool.models import User, Car, CarManager
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route('/book', methods=['GET', 'POST'])
def book():
    bookings = CarManager.query.all()
    form = BookForm()
    if form.validate_on_submit():
        booking = CarManager(day=form,
                             car=form.car.data, user=current_user)
        db.session.add(booking)
        try:
            db.session.commit()
            flash('Your have booked a car!', 'success')
        except:
            db.session.rollback()
            flash('Booking not created', 'error')
    return render_template('book.html', bookings=bookings,
                           form=form, legend='New Booking')


@app.route('/cars', methods=['GET'])
def cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)

@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
