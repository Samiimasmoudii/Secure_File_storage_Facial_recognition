from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)


def get_icon(filename):
    _, extension = os.path.splitext(filename.lower())
    if extension == '.pdf':
        return 'pdf.png'
    elif extension in ('.jpg', '.jpeg', '.png', '.gif'):
        return 'image.png'
    else:
        return 'cloud.png'  # Default icon for unknown file types

@views.route('/', methods=['get','POST'])
def home():
    print(current_user.is_authenticated)
    return render_template('login.html') 

@views.route('/home', methods=['get','POST'])       
@login_required
def drive():
    print(current_user.is_authenticated)
    
    if current_user.is_authenticated:
        # If the user is authenticated, you can access their ID and name
        user_id = current_user.id
        username = current_user.first_name
        
        print(f"User ID: {user_id}, Username: {username}")
    else:
        print("Not logged in")
    
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    print("Uploaded files are: ", files)

    # Prepare a list of dictionaries containing filename and its corresponding icon
    file_icons = [{'name': file, 'icon': get_icon(file),} for file in files]

    return render_template('drive.html', user=current_user, files=file_icons) 

@views.route('/upload', methods=['GET', 'POST'])       
@login_required
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file : 
            print ("File Exists")
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully', 'success')
            return redirect(url_for('views.drive'))  # Redirect to the drive page after upload
    return render_template('drive.html')

@views.route('/account', methods=['get','POST'])       
@login_required
def account():
    print(current_user.is_authenticated)
    
    if current_user.is_authenticated:
        # If the user is authenticated, you can access their ID and name
        user_id = current_user.id
        username = current_user.first_name
        
        flash(f"User ID: {user_id}, Username: {username}")
    else:
        flash("Not logged in")
    
    return render_template('account.html', user=current_user) 
