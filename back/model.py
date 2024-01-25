from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    """
    Return a random UUID for the primary key of a model
    """
    return uuid4().hex

class User(db.Model):
    """
    User model for storing user related details
    """
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    first_name = db.Column(db.String(345), nullable=False)
    last_name = db.Column(db.String(345), nullable=False)
    email = db.Column(db.String(345), unique=True, nullable=False)
    password = db.Column(db.String(345), nullable=False)