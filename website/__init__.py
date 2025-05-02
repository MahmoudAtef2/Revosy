"""
Flask Application Factory and Configuration
This module initializes the Flask application, database, and login manager.
"""

import os
from os import path, makedirs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# Constants
DB_NAME = "database.db"
UPLOAD_FOLDER = path.join('website', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_app():
    """
    Application factory function that creates and configures the Flask app.

    Returns:
        Flask: The configured Flask application instance
    """
    app = Flask(__name__)

    # Configuration Settings
    app.config.update(
        # Use environment variable in production
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{DB_NAME}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Disables modification tracking overhead
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # 5MB upload limit
        ALLOWED_EXTENSIONS=ALLOWED_EXTENSIONS
    )

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Configure login manager
    login_manager.login_view = "auth.sign_in"
    login_manager.login_message = "Please log in to access this page"
    login_manager.login_message_category = "error"

    # Register blueprints
    from . import views, auth
    app.register_blueprint(views.views)
    app.register_blueprint(auth.auth)

    # Create required directories and database
    with app.app_context():
        create_database(app)
        ensure_upload_folder()

    return app


def create_database(app):
    """
    Initialize database if it doesn't exist.

    Args:
        app (Flask): The Flask application instance
    """
    if not path.exists(f"website/{DB_NAME}"):
        db.create_all()
        print(f"Created database at website/{DB_NAME}")


def ensure_upload_folder():
    """
    Ensure the upload directory exists.
    Creates the directory if it doesn't exist.
    """
    if not path.exists(UPLOAD_FOLDER):
        makedirs(UPLOAD_FOLDER)
        print(f"Created upload directory at {UPLOAD_FOLDER}")


@login_manager.user_loader
def load_user(id):
    """
    Flask-Login user loader callback.

    Args:
        id (str): The user ID to load

    Returns:
        User: The User instance if found, None otherwise
    """
    from .models import User  # Import here to avoid circular imports
    return User.query.get(int(id))
