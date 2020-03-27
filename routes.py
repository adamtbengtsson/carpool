import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm, AddCarForm, UpdateCar, NewBooking
from flaskblog.models import User, Post, Comment, Car, Comment2, CarManager
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_

@app.route("/")
@app.route("/home")
def home():
    bookings = CarManager.query.order_by(CarManager.date_posted.desc()).all()
    return render_template('home.html', bookings=bookings)


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


def save_compressed_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_raw_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    form_picture.save(picture_path)

    return picture_fn

def save_raw_picture_car(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/car_pics', picture_fn)

    form_picture.save(picture_path)

    return picture_fn


@app.route("/bookings", methods=['GET'])
@login_required
def bookings():
    name = current_user.username
    bookings = CarManager.query.filter_by(user=current_user).order_by(CarManager.day).all()
    return render_template('bookings.html', bookings=bookings)


@app.route("/cars", methods=['GET'])
@login_required
def cars():
    searchword = request.args.get('key', '')
    if searchword is not '':
        cars = Car.query.filter(or_(Car.car_name.contains(searchword),
                                    Car.fuel.contains(searchword),
                                    Car.seats.contains(searchword))
                                ).all()
        if cars:
            return render_template('cars.html', cars=cars, searchword=searchword)
        else:
            flash('No cars related to search found, showing all cars instead', 'danger')
            cars = Car.query.all()
            return render_template('cars.html', cars=cars)
    else:
        cars = Car.query.all()
        return render_template('cars.html', cars=cars)
    #cars = Car.query.order_by(Car.car_name).all()
    #return render_template('cars.html', cars=cars)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # picture_file = save_compressed_picture(form.picture.data)
            picture_file = save_raw_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.std_destination = form.std_destination.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.std_destination.data = current_user.std_destination
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/cars/add", methods=['GET', 'POST'])
@login_required
def add_car():
    form = AddCarForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_raw_picture_car(form.picture.data)
            car = Car(user=current_user, car_name=form.car_name.data, model=form.model.data, license_plate=form.license_plate.data.upper(), fuel=form.fuel.data, seats=form.seats.data, info=form.info.data, owner=current_user, image_file = picture_file)
        else:
            car = Car(user=current_user, car_name=form.car_name.data, model=form.model.data, license_plate=form.license_plate.data.upper(), fuel=form.fuel.data, seats=form.seats.data, info=form.info.data, owner=current_user)
        db.session.add(car)
        db.session.commit()
        flash('Your car has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_car.html', title='Add Car',
                           form=form, legend='Add Car')


@app.route("/choose_car", methods=['GET'])
@login_required
def choose_car():
    cars = Car.query.order_by(Car.car_name).all()
    return render_template('choose_car.html', cars=cars)


@app.route("/new_booking/<int:car_id>", methods=['GET', 'POST'])
@login_required
def new_booking(car_id):
    car = Car.query.get_or_404(car_id)
    form = NewBooking()
    form.combo.data = f'{car.id}{form.day.data}'
    form.update.data = False
    if form.validate_on_submit():

        booking = CarManager(user=current_user,
                             car=car,
                             day=form.day.data,
                             destination=form.destination.data,
                             combination=form.combo.data)

        db.session.add(booking)
        db.session.commit()
        flash('Your car is booked!', 'success')
        return redirect(url_for('home'))

    form.destination.data = current_user.std_destination
    return render_template('new_booking.html', title='Book Car',
                           form=form, legend='Book Car', car=car)


@app.route("/car/<int:car_id>", methods=['GET', 'POST'])
def car(car_id):
    car = Car.query.get_or_404(car_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated: # you can only comment if you're logged in
            comment = Comment2(content=form.content.data, user=current_user, car=car)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been created!', 'success')
            return redirect(f'/car/{car.id}')
        else:
            flash('You are not logged in. You need to be logged in to be able to comment!', 'danger')
    return render_template('car.html', title=car.car_name, car=car, form=form)



@app.route("/car/<int:car_id>/update", methods=['GET', 'POST'])
@login_required
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    if  car.user != current_user:
        abort(403)
    form = UpdateCar()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_raw_picture_car(form.picture.data)
            car.image_file = picture_file
        car.fuel = form.fuel.data
        car.seats = form.seats.data
        car.info = form.info.data
        car.car_name = form.car_name.data
        car.license_plate = form.license_plate.data
        car.model = form.model.data

        db.session.commit()
        flash('Your car has been updated!', 'success')
        return redirect(url_for('car', car_id=car.id))

    elif request.method == 'GET':
        form.fuel.data = car.fuel
        form.seats.data = car.seats
        form.info.data = car.info
        form.model.data = car.model
        form.license_plate.data = car.license_plate
        form.car_name.data = car.car_name
        form.picture.data = car.image_file
    return render_template('add_car.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/bookings/<int:booking_id>", methods=['GET'])
@login_required
def booking(booking_id):
    booking = CarManager.query.filter_by(id=booking_id).first()
    return render_template('booking.html', title=booking.car.car_name, booking=booking)


@app.route("/booking/<int:booking_id>/update", methods=['GET', 'POST'])
@login_required
def update_booking(booking_id):
    carmanager = CarManager.query.get_or_404(booking_id)
    form = NewBooking()
    if carmanager.user != current_user:
        abort(403)

    if form.day.data == carmanager.day:
        form.update.data = True
    else:
        form.update.data = False
    form.update.date = False
    form.combo.data = f'{carmanager.car_id}{form.day.data}'
    car = carmanager.car

    if form.validate_on_submit():
        carmanager.destination = form.destination.data
        carmanager.day = form.day.data
        carmanager.combination = form.combo.data
        db.session.commit()
        flash('Your booking has been updated', 'success')
        return redirect(url_for('booking', booking_id=carmanager.id))
    elif request.method == 'GET':
        form.destination.data = carmanager.destination
        form.day.data = carmanager.day
    return render_template('new_booking.html', title='Update Booking',
                           form=form, car=car, legend='Update Booking')


@app.route("/car/<int:car_id>/delete", methods=['POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user != current_user:
        abort(403)
    CarManager.query.filter_by(car=car).delete()
    db.session.delete(car)
    db.session.commit()
    flash('Your car has been removed!', 'success')
    return redirect(url_for('home'))


@app.route("/booking/<int:booking_id>/delete", methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = CarManager.query.get_or_404(booking_id)
    if booking.user != current_user:
        abort(403)
    db.session.delete(booking)
    db.session.commit()
    flash('Your booking has been cancelled', 'success')
    return redirect(url_for('home'))
