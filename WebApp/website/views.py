from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import subprocess
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
    encrypted_filename = base_filename + '_encrypted' + extension
    with open(encrypted_filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
        
    
    print(f"Encrypted file saved as: {encrypted_filename}")

    return encrypted_filename  # Return the path of the encrypted file




def decrypt_file(original_filename, encryption_key) :
    # Load the encryption key from the key file
   

    # Initialize the Fernet instance with the key
    fernet = Fernet(encryption_key)
    base_filename, extension = os.path.splitext(original_filename)
    # Read the encrypted data from the file
    encrypted_file_path = base_filename + extension
    
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data)

    # Determine the original file path and extension
    
    decrypted_file_path = base_filename + "_decrypted" + extension

    # Write the decrypted data to a new file
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    print("File decrypted successfully:", decrypted_file_path)





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
    
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file:
            print('File Exists, Begin Uploading...')
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(current_app.config['TEMP_FILE_FOLDER'], filename))
            flash('File Uploading...', 'success')
            
            #file_relative_path = os.path.relpath(file.name, os.getcwd())
            encrypted_filename = encrypt_file(os.path.join(current_app.config['TEMP_FILE_FOLDER'], filename), key)
            
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
