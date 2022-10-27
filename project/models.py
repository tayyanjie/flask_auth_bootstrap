from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    """Creates a User table for auth"""

    # Each user has an id as a primary key for the Users table
    id = db.Column(db.Integer, primary_key=True)

    # email should be unqiue
    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(500))
    name = db.Column(db.String(100))