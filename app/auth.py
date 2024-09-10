from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, StudyRoom, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import os
import secrets
from flask import current_app as app
from PIL import Image
from flask import session, g
from werkzeug.utils import secure_filename
 

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
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('Email does not exist.', category='danger')


    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
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

#Modification required
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot-password.html')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/profile_pic', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        profilepicture = request.files['profilepicture']

        # Validation checks
        if not email or not username:
            flash('Email and username are required', category='error')
            return redirect(url_for('auth.account'))

        # Check if email already exists
        user = User.query.filter_by(email=email).first()
        if user and user.id != current_user.id:
            flash('Email already exists. Please choose a different one.', category='error')
            return redirect(url_for('auth.account'))

        # Check if username already exists
        user = User.query.filter_by(username=username).first()
        if user and user.id != current_user.id:
            flash('Username already exists. Please choose a different one.', category='error')
            return redirect(url_for('auth.account'))

        # Update email and username
        current_user.email = email
        current_user.username = username

       # Handle profile picture upload
        if profilepicture and allowed_file(profilepicture.filename):
            filename = save_picture(profilepicture)
            current_user.profilepicture = filename
        else:
            flash('File type not allowed. Please upload a PNG, JPG, JPEG, or GIF image.', category='error')
            db.session.rollback()
            return redirect(url_for('auth.account'))

        # Save changes to the database
        try:
            db.session.commit()
            flash('Your account has been updated!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your account. Please try again.', 'danger')

        return redirect(url_for('auth.account'))

    # Handle GET request
    if current_user.profilepicture:
        profilepicture = url_for('static', filename='images/profile_pic/' + current_user.profilepicture)
    else:
        profilepicture = url_for('static', filename='images/profile_pic/default.jpg')

    return render_template('account.html', user=current_user, profilepicture=profilepicture)


def generate_current_room():
    """
    Retrieves the current room based on the room_id stored in the session.
    If the room_id is not in the session, it returns None.
    """
    room_id = session.get('room_id')

    if room_id is None:
        return None

    room = StudyRoom.query.get(room_id)

    if room is None:
        return None

    g.current_room = room
    
    return room
@auth.route('/dashboard')
@login_required
def dashboard():
    room = generate_current_room()  # This fetches the current room, if any
    study_rooms = StudyRoom.query.all()  # Fetch the list of all study rooms
    if room is None:
        app.logger.debug('Room not found')
    return render_template("dashboard.html", user=current_user, current_room=room, study_rooms=study_rooms)



