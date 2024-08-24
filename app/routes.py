from flask import request, render_template, redirect, url_for
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """
    Handles user sign-up by processing form data and creating a new user account.
    
    Parameters:
    - request.method (str): The HTTP method used to make the request.
    - request.form (dict): A dictionary containing form data.
    
    Returns:
    - redirect: Redirects the user to the login page upon successful sign-up.
    - render_template: Renders the sign-up page if the request method is GET.
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)


        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

       
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('signup.html')
    

@app.route('/login')
def login():
    """
    Handles user login by rendering the login page.

    Parameters:
    - None

    Returns:
    - render_template: Renders the login page.
    """
    return render_template('login.html')