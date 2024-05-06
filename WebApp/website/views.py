from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app,send_from_directory,send_file
from .models import File
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from datetime import datetime
from . import db
import subprocess
import shutil
import os

views = Blueprint('views', __name__)
with open('WebApp\instance\key.txt', 'rb') as f:
        key = f.read()

def get_icon(filename):
    _, extension = os.path.splitext(filename.lower())
    if extension == '.pdf':
        return 'pdf.png'
    elif extension in ('.jpg', '.jpeg', '.png', '.gif'):
        return 'image.png'
    else:
        return 'cloud.png'  # Default icon for unknown file types
    


def decrypt_file(encrypted_filename, encryption_key):
    try:
        # Initialize the Fernet instance with the key
        fernet = Fernet(encryption_key)

        # Read the encrypted data from the file in the uploads folder
        encrypted_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], encrypted_filename)
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)

        # Determine the original file path and extension
        base_filename, extension = os.path.splitext(encrypted_filename)
        original_filename = base_filename.rsplit('_encrypted', 1)[0] + extension
        
        # Write the decrypted data to a new file in the temporary folder
        decrypted_file_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], original_filename)
        with open(decrypted_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print("File decrypted successfully:", decrypted_file_path)

        # Pass the path of the decrypted file to the download function
        return decrypted_file_path
    
    except Exception as e:
        print("Error decrypting file:", str(e))
        return None

def encrypt_file(filename, key):
    try:
        # Read the file content
        with open(filename, 'rb') as file:
            original = file.read()
            print("File loaded successfully")
    except FileNotFoundError:
        print("Error: File not found")
        return None  # Return None if file is not found

    # Encrypt the file content
    fernet = Fernet(key)
    encrypted = fernet.encrypt(original)
    print("File encrypted successfully")

    # Decompose the filename and extension
    base_filename, extension = os.path.splitext(filename)

    # Rename the encrypted file with the original extension
    encrypted_filename = base_filename + extension
    with open(encrypted_filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
        
    
    print(f"Encrypted file saved as: {encrypted_filename}")

    return encrypted_filename  # Return the path of the encrypted file








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

    # Get filenames associated with the current user from the database
    user_files = File.query.filter_by(user_id=current_user.id).with_entities(File.file_name).all()

    print("Uploaded files are: ", user_files)

    # Prepare a list of dictionaries containing filename and its corresponding icon
    file_icons = [{'name': file.file_name, 'icon': get_icon(file.file_name)} for file in user_files]

    return render_template('drive.html', user=current_user, files=file_icons)
 


#@views.route('/download/<path:encrypted_filename>',methods=['GET','POST'])
# def download(encrypted_filename): 
    #print('download button pressed')
    #decrypted_filepath = decrypt_file(encrypted_filename,key)
    #print('File decrypted succesfully')
    #directory, filename = os.path.split(decrypted_filepath)
    #print('File ready to download')
    #if "_encrypted" in filename:
    #    filename = filename.replace("_encrypted", "")
    #print (directory)
    #print(filename)
    #return send_from_directory(directory, filename)
    #return send_from_directory('/uploads/temp',filename)
    #return render_template('drive.html', user=current_user)
@views.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    decrypted_filepath = decrypt_file(filename, key)
    if decrypted_filepath:
        directory, filename = os.path.split(decrypted_filepath)
        #if "_encrypted" in filename:
           # filename = filename.replace("_encrypted", "")
        filepath=os.path.join('.\download', filename)
        return send_file(filepath, as_attachment=False)
    else:
        # Handle decryption error
        flash("Error downloading file: decryption failed", 'error')
        return redirect(url_for('views.drive'))



@views.route('/upload', methods=['GET', 'POST'])       
@login_required
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
    
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file:
            print('File Exists, Begin Uploading...')
            filename = secure_filename(file.filename)
            
            file_path = file.save(os.path.join(current_app.config['TEMP_FILE_FOLDER'], filename))
            
            #file_stat = os.stat(file_path)
            #file_size=file_stat.st_size
            
            #print('File size is ', file_size)
            flash('File Uploading...file_path)uccess')
            print ('File save in ', file_path)
            #file_relative_path = os.path.relpath(file.name, os.getcwd())
            encrypted_filename = encrypt_file(os.path.join(current_app.config['TEMP_FILE_FOLDER'], filename), key)
            new_file = File(
                    file_name=os.path.basename(encrypted_filename),  # Use the encrypted filename
                    #file_size=file_size,  # Get the file size
                    file_path=os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(encrypted_filename)),  # Use the path where the file is saved
                    upload_date=datetime.now(),  # Set the upload date
                    user=current_user  # Link the file to the current user
                )
            db.session.add(new_file)
            db.session.commit()

            os.rename(encrypted_filename, os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(encrypted_filename)))
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


