"""
Authentication Blueprint
Handles user registration, login, and logout functionality.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
import re

auth = Blueprint("auth", __name__)


def is_password_complex(password):
    """
    Validate password complexity.

    Args:
        password (str): The password to validate

    Returns:
        bool: True if password meets complexity requirements, False otherwise
    """
    return (len(password) >= 8 and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password))


@auth.route('/signin', methods=['GET', 'POST'])
def sign_in():
    """
    Handle user sign-in.

    GET: Display sign-in form
    POST: Process sign-in form and authenticate user
    """

    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash("Signed in successfully", category='success')

            # Redirect to home
            return redirect(url_for('views.home'))

        flash('Invalid email or password', category='error')

    return render_template("Signin.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    """
    Handle user registration.

    GET: Display registration form
    POST: Process registration form and create new user
    """

    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Input validation
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if len(username) < 3:
            flash('Username must be at least 3 characters', category='error')
        elif username_exists:
            flash('Username already in use', category='error')
        elif not re.match(email_pattern, email):
            flash('Invalid email format', category='error')
        elif email_exists:
            flash('Email already registered', category='error')
        elif not is_password_complex(password1):
            flash('Password must be 8+ chars with uppercase and number',
                  category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            # Create new user
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(
                    password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully! Please sign in', category='success')
            return redirect(url_for('auth.sign_in'))

    return render_template("Signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    """
    Handle user logout.
    Only accessible to authenticated users.
    """
    logout_user()
    flash("You have been logged out", category='success')
    return redirect(url_for('views.home'))
