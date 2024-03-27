from flask import Blueprint, render_template, request,flash,redirect , url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


# When generating a hash, you cannot find the original oassword through the hashed password
# You're never storing the password in plain text
#you can only check if the stored password si equal to the hashed password 

auth = Blueprint('auth',__name__ )
@auth.route( '/login' , methods=['POST' ,'get' ])
def login():
    data = request.form
    print(data)
    
    return render_template( 'login.html')






@auth.route('/logout')
def logout():
    return render_template( 'logout.html')


@auth.route('/signup',methods=['POST', 'get'])
def signup():
    if request.method == 'POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        if len(email)<4:
           flash('Email must be greater than 4 character' , category ='error')
        elif len(firstName)<4:
           flash('First Name must be greater than 4 character' , category ='error')
        elif len(password1)<7:
           flash('Password must be greater than 7 characters' , category ='error')
        elif password1 != password2: 
            flash('Password dont match' , category ='error')
        else:
            new_user = User(email=email, first_name=firstName,password=generate_password_hash(password1,method='pbkdf2:sha256',salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created' , category ='success')
            #Redirect to the home page
            return redirect(url_for('views.home'))
         
    return render_template( 'sign_up.html')
