from flask import render_template,redirect,url_for,request,flash
from .. import db
from . import auth
from ..models import User
from flask_login import login_required,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash


@auth.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email ).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('password is incorrect',category='error')    
        else:
            flash('Email does not exist!',category='error')

    return render_template('auth/login.html',user = current_user)



@auth.route('/sign_up',methods = ['POST','GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use',category='error')
        elif username_exists:
            flash('Username is a already taken', category='error')
        elif password1 != password2:
            flash('passwords do not match!', category='error') 
        elif len(username) < 4:
            flash('Username is too short' , category='error')
        elif len(password1) < 6:
            flash('Password is too short', category='error')
        else:
            new_user = User(email = email,username = username ,password = generate_password_hash( password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember =True)
            flash('Account successfully created!',category='success') 
            return redirect(url_for('main.index'))           
            

    return render_template('auth/register.html',user = current_user)


    
@auth.route('/sign_out')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('main.index'))    