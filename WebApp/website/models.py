from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__='User'
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    user_id=db.Column(db.Integer, db.ForeignKey('User.id'))
    
class File(db.Model):
    __tablename__ = 'file'  # Use lowercase for the table name
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)  # Correct casing for the table name
    user = db.relationship('User', backref=db.backref('files', lazy=True)) # lazy allows the user class to be loaded without needing to load all the files. THe files will be loaded when needed 

    def __repr__(self): # Use for debugging 
        return f"File(id={self.id}, filename='{self.filename}', user_id={self.user_id})"
