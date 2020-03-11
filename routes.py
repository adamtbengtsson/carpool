import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from carpool import app, db, bcrypt
from carpool.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from flaskcarpoolblog.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/book')
def book():
    return render_template('book.html')
