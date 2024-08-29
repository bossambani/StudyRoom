from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash ('Logged in Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')


    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password1')
        password1 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        
        elif password != password1:
            flash('Passwords don\'t match.', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category ='danger')
        
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', category = 'danger')
            
        elif len(lastname) < 2:
            flash('Last name must be greater than 1 character.', category ='danger')
            
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category = 'danger')
            
        elif len(password) < 7:
            flash('Password must be greater than 6 characters.', category = 'danger')
           
        else:
            new_user = User(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category = 'success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot-password.html')