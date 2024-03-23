from flask import Blueprint, render_template, request,flash

auth = Blueprint('auth',__name__ )
@auth.route( '/login' , methods=['POST' ,'GET' ])
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
            flash('Account Created' , category ='success')
         
    return render_template( 'sign_up.html')
