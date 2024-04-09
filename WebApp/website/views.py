from flask import Blueprint, render_template

from flask_login import login_required, current_user
from flask import Blueprint, render_template, request,flash,redirect , url_for,session
views = Blueprint('views', __name__)

@views.route('/', methods=['get','POST'])
def home ():
    print(current_user.is_authenticated)
    return render_template('login.html') 

@views.route('/home', methods=['get','POST'])       
@login_required
def drive ():
    print(current_user.is_authenticated)
    
    if current_user.is_authenticated:
        # If the user is authenticated, you can access their ID and name
        user_id = current_user.id
        username = current_user.first_name
        
        print( f"User ID: {user_id}, Username: {username}")
    else:
        print("Not logged in")
    
    return render_template('drive.html',user=current_user) 


@views.route('/account', methods=['get','POST'])       
@login_required
def account ():
    print(current_user.is_authenticated)
    
    if current_user.is_authenticated:
        # If the user is authenticated, you can access their ID and name
        user_id = current_user.id
        username = current_user.first_name
        
        flash( f"User ID: {user_id}, Username: {username}")
    else:
        flash("Not logged in")
    
    return render_template('account.html',user=current_user) 

