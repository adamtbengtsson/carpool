import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm, AddCarForm
from flaskblog.models import User, Post, Comment, Car
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



@app.route("/bookings", methods=['GET'])
@login_required
def bookings():
    name = current_user.username
    posts = Post.query.filter_by(user=current_user).order_by(Post.date_posted).all()
    return render_template('bookings.html', posts=posts)

@app.route("/cars", methods=['GET'])
@login_required
def cars():
    searchword = request.args.get('key', '')
    if searchword is not '':
        cars = Car.query \
            .filter(or_(Car.car_name.contains(searchword),
                        Car.fuel.contains(searchword),
                        Car.seats.contains(searchword))) \
            .all()
        return render_template('cars.html', cars=cars, searchword=searchword)
    else:
        print('\n\n, key not found, \n\n')
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
            picture_file = save_raw_picture(form.picture.data)
            car = Car(car_name=form.car_name.data, model=form.model.data, license_plate=form.license_plate.data, fuel=form.fuel.data, seats=form.seats.data, info=form.info.data, picture_file = picture_file)
        else:
            car = Car(car_name=form.car_name.data, model=form.model.data, license_plate=form.license_plate.data, fuel=form.fuel.data, seats=form.seats.data, info=form.info.data)
        db.session.add(car)
        db.session.commit()
        flash('Your car has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_car.html', title='Add Car',
                           form=form, legend='Add Car')


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

