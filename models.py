from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Pet Class"""
    __tablename__ = "pets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(30),
                           nullable=False)
    species = db.Column(db.String(30),
                           nullable=False)
    photo_url = db.Column(db.String, default = "https://images.pexels.com/photos/356079/pexels-photo-356079.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260")
    age = db.Column(db.String, nullable=False)
    notes = db.Column(db.String(400))
    available = db.Column(db.Boolean, default=True)