from .db_models import User,Statements
from.import db
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask, render_template,request,url_for,flash, redirect,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

authentication=Blueprint("authentication",__name__,static_folder="static",template_folder="templates")

@authentication.route('/login',methods=['GET','POST'])
def login():
    global users
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('pass')
        users=User.query.filter_by(email=email).first() #checking user in database
        if users:
            if check_password_hash(users.password, password): 

                
                login_user(users,remember=True)
                return redirect(url_for('routes.home'))
            else:

                flash("Password Incorrect",category='error')
        else:

            flash("User does not exist",category='error')       
    return render_template('login.html')

@authentication.route('/', methods=['GET', 'POST'])
def signup():
   
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        password=request.form.get('password')

        user_name_check=User.query.filter_by(user_name=name).first()
        email_check=User.query.filter_by(email=email).first()
        if user_name_check:
            flash("User exists",category='error')
        elif email_check:
            flash("Email already exist",category='error')
        else:
           
            new_user=User(user_name=name,email=email,phone=phone,password=generate_password_hash(password, method='sha256')) #creating hash of password for validation of user
            
            db.session.add(new_user)
            
            db.session.commit()
            
            login_user(new_user,remember=True)
            
            flash("Registered Successfully",category='success')
            
            return redirect(url_for('routes.home'))
        

    return render_template('create_acc.html')


@authentication.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))