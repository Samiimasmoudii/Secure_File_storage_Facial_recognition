from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path, urandom
from flask_login import LoginManager
db= SQLAlchemy()
DB_NAME= "database.db"


def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'  
    app.config['UPLOAD_FOLDER'] = r'WebApp\website\uploads'
    app.config['STATIC_URL_PATH'] = '/static'
    app.config['STATIC_FOLDER'] = 'static'

    upload_dir = os.path.join(app.instance_path, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
  
    db.init_app(app)
  
    
    from website.views import views
    from website.auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from website.models import User, Note
    with app.app_context():
        db.create_all()
    
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app





def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # Create all tables
        db.create_all(app=app)

        # If the tables are created successfully, print a success message
        print('Database created successfully')

        # Ensure that the User table is created before the Note table
        from .models import User, Note
        db.session.commit()  # Commit any changes before creating tables
        db.reflect()
        db.create_all(app=app, tables=[User.__table__])

        # Create all other tables
        db.create_all(app=app, tables=[Note.__table__])

        print('All tables created successfully')
    else:
        print('Database already exists')