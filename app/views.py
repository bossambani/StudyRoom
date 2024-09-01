from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required,  current_user
from app.auth import dashboard


views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return render_template("home.html", user=current_user)
