from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
db= SQLAlchemy()
DB_NAME= "database.db"


def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = 'kfjshflakjhflkj'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'    
    db.init_app(app)
    
    from website.views import views
    from website.auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    from website.models import User, Note
     
    return app
def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('Database created successfully')