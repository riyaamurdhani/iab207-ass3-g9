from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db, bcrypt, mail
from app.models.user import User
from flask_mail import Message
from flask_login import login_user, logout_user, login_required

import random, string

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        middlename = request.form.get('middlename', '')
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        contact_number = request.form['contact_number']
        address = request.form['address']

        raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        hashed_password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

        user = User(
            firstname=firstname,
            middlename=middlename,
            lastname=lastname,
            username=username,
            email=email,
            password=hashed_password,
            contact_number=contact_number,
            address=address
        )

        db.session.add(user)
        db.session.commit()

        msg = Message('Your Account Credentials',
                      sender='noreply@example.com',
                      recipients=[email])
        msg.body = f"Hello {username},\n\nYour login credentials:\nEmail: {email}\nPassword: {raw_password}"
        mail.send(msg)

        flash('User registered and credentials sent to email.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index.home_page'))
        else:
            flash('Login failed. Check your username or password.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
