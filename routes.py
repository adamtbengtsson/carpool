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
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts)


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
                        Car.seats.contains(searchword))).all()
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


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content_type=form.content_type.data, content=form.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


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





@app.route("/new_booking", methods=['GET', 'POST'])
@login_required
def new_booking():
    form = NewBooking()
    if form.validate_on_submit():
        car = Car.query.filter_by(id=int(form.car.data)).first()
        booking = CarManager(user=current_user, car=car, day=form.day.data, destination=form.destination.data)


        db.session.add(booking)
        db.session.commit()
        flash('Your car is booked!', 'success')
        return redirect(url_for('home'))
    optionsList = []
    for option in Car.query.all():
        optionsList.append((f'{option.id}',
                            f'{option.car_name.upper()} - {option.model}, {option.license_plate}, Seats: {option.seats}, Fuel %: {option.fuel}'))

        form.car.choices.append((f'{option.id}',
                            f'{option.car_name.upper()} - {option.model}, {option.license_plate}, Seats: {option.seats}, Fuel %: {option.fuel}'))

    form.destination.data = current_user.std_destination
    return render_template('new_booking.html', title='Book Car',
                           form=form, legend='Book Car')


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated: # you can only comment if you're logged in
            comment = Comment(content=form.content.data, user=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(f'/post/{post.id}')
        else:
            flash('You are not logged in. You need to be logged in to be able to comment!', 'danger')
    return render_template('post.html', title=post.title, post=post, form=form)


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


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.content_type = form.content_type.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.content_type.data = post.content_type
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

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



@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))



@app.route("/car/<int:car_id>/delete", methods=['POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user != current_user:
        abort(403)
    db.session.delete(car)
    db.session.commit()
    flash('Your car has been removed!', 'success')
    return redirect(url_for('home'))


@app.route("/car/<int:car_manager_id>/delete", methods=['POST'])
@login_required
def delete_booking(car_manager_id):
    car = Car.query.get_or_404(car_manager_id)
    if car.user != current_user:
        abort(403)
    db.session.delete(car)
    db.session.commit()
    flash('Your booking has been cancelled', 'success')
    return redirect(url_for('home'))

