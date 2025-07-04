from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from bson.objectid import ObjectId
from .models import User
from . import mongo

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if mongo.db.users.find_one({'email': email}):
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)
        mongo.db.users.insert_one({'email': email, 'password': hashed_pw})
        flash('Registration successful!')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = mongo.db.users.find_one({'email': email})

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            remember = 'remember' in request.form
            login_user(user, remember=remember)
            return redirect(url_for('main.dashboard'))

        flash('Invalid credentials')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
