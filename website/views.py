"""
Views Blueprint
Handles core application views and venue management.
"""

from flask import (Blueprint, render_template, redirect,
                   url_for, request, flash, current_app)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import Venues
import os

views = Blueprint('views', __name__)


def allowed_file(filename):
    """
    Check if a filename has an allowed extension.

    Args:
        filename (str): The filename to check

    Returns:
        bool: True if extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


@views.route('/')
@views.route('/home')
def home():
    """
    Render the home page with recent venues.
    """
    venues = Venues.query.order_by(Venues.date_created.desc()).limit(6).all()
    return render_template('index.html', user=current_user, venues=venues)


@views.route('/venues')
@login_required
def venues():
    """
    Render the venues listing page.
    Requires authentication.
    """
    venues = Venues.query.order_by(Venues.date_created.desc()).all()
    return render_template("venues.html", user=current_user, venues=venues)


@views.route('/create-venue', methods=['GET', 'POST'])
@login_required
def create_venue():
    """
    Handle venue creation.

    GET: Display venue creation form
    POST: Process form and create new venue
    Requires authentication.
    """
    if request.method == 'POST':
        # Validate required fields
        required_fields = ['title', 'location', 'price', 'contact_number']
        if not all(field in request.form for field in required_fields):
            flash('Please fill all required fields', 'error')
            return redirect(request.url)

        # Process file upload
        file = request.files.get('image')
        if not file or file.filename == '':
            flash('No image selected', 'error')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Allowed image types: png, jpg, jpeg, gif', 'error')
            return redirect(request.url)

        try:
            # Secure filename and save
            filename = secure_filename(file.filename)
            filepath = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Create and save venue
            venue = Venues(
                title=request.form['title'],
                location=request.form['location'],
                price=int(request.form['price']),
                contact_number=request.form['contact_number'],
                image=filename,
                author=current_user.id
            )
            db.session.add(venue)
            db.session.commit()

            flash('Venue created successfully!', 'success')
            return redirect(url_for('views.venues'))

        except ValueError:
            flash('Price must be a number', 'error')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating venue: {str(e)}")
            flash('Error creating venue', 'error')

    return render_template('create_venue.html', user=current_user)


@views.route('/delete-venue/<int:id>', methods=['POST'])
@login_required
def delete_venue(id):
    """
    Delete a venue.

    Args:
        id (int): The ID of the venue to delete

    Requires authentication and ownership of the venue.
    """
    venue = Venues.query.get_or_404(id)

    # Authorization check
    if venue.author != current_user.id:
        flash('You can only delete your own venues', 'error')
        return redirect(url_for('views.venues'))

    try:
        # Delete associated image file if it exists
        if venue.image and os.path.exists(os.path.join(
                current_app.config['UPLOAD_FOLDER'], venue.image)):
            os.remove(os.path.join(
                current_app.config['UPLOAD_FOLDER'], venue.image))

        # Delete from database
        db.session.delete(venue)
        db.session.commit()
        flash('Venue deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting venue: {str(e)}")
        flash('Error deleting venue', 'error')

    # Redirect back to where the request came from
    referrer = request.referrer or url_for('views.venues')
    return redirect(referrer)


@views.route('/profile')
@login_required
def profile():
    """
    Render the user profile page with their venues.
    Requires authentication.
    """
    user_venues = Venues.query.filter_by(
        author=current_user.id).order_by(Venues.date_created.desc()).all()
    return render_template("profile.html", user=current_user, venues=user_venues)
