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
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)  # Correct casing for the table name
    user = db.relationship('User', backref=db.backref('files', lazy=True)) # Establish a one-to-many relationship with the User model
   
   
    def __repr__(self): # Use for debugging 
        return f"File(id={self.id}, file_name='{self.file_name}', user_id={self.user_id})"