"""
Database Models
Defines the User and Venue database models with relationships.
"""

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    """
    User model representing application users.

    Attributes:
        id (int): Primary key
        username (str): Unique username
        email (str): Unique email
        password (str): Hashed password
        user_image (str): Path to profile image
        date_created (DateTime): Account creation timestamp
        venues (relationship): One-to-many relationship with Venues
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    user_image = db.Column(db.String(20),
                           nullable=False,
                           default='static/images/user_image.jpg')
    date_created = db.Column(db.DateTime(timezone=True),
                             default=func.now())
    venues = db.relationship('Venues',
                             backref='user',
                             lazy=True,
                             cascade='all, delete-orphan')


class Venues(db.Model):
    """
    Venue model representing event venues.

    Attributes:
        id (int): Primary key
        title (str): Venue name/title
        image (str): Path to venue image
        price (int): Daily price
        location (str): Venue location
        contact_number (str): Contact phone number
        date_created (DateTime): Creation timestamp
        author (int): Foreign key to User who created the venue
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(150),
                      nullable=False,
                      default='static/images/post_image.jpg')
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),
                             default=func.now())
    author = db.Column(db.Integer,
                       db.ForeignKey('user.id', ondelete="CASCADE"),
                       nullable=False)
