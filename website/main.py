from flask import Flask, render_template,request,url_for,flash, redirect
import pickle
from text_cleaner import cleaning
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from trait_provider import trait_provider
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,login_required,current_user,UserMixin,LoginManager,current_user
from  werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI']= "mysql://root:tool@localhost:3306/personality_clasifier"
db=SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
         id=db.Column('user-id',db.Integer,primary_key=True)
         user_name=db.Column('user_name',db.String(20),unique=True,nullable=False)
         email=db.Column('email',db.String(200),unique=True,nullable=False)
         phone=db.Column('phone',db.String(12),unique=True,nullable=False)
         password=db.Column('pass',db.String(10000),nullable=False)
         forign=db.relationship('Statements',backref='author',lazy=True)
     
             

class Statements(db.Model,UserMixin):
    id=db.Column('sent_id',db.Integer,primary_key=True)
    sent=db.Column('sent',db.Text,nullable=False)
    trait=db.Column('personality_key',db.Text,nullable=False)
    user_id=db.Column("user_id",db.Integer,db.ForeignKey(User.id), nullable=False)



model = pickle.load(open('./static/model.pkl','rb'))
matrix_features= pickle.load(open('./static/matrix_feature.pkl','rb'))
label_enc = pickle.load(open('./static/label_en.pkl','rb'))

#Sign up ---Creating account---

@app.route('/', methods=['GET', 'POST'])
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
            
            return redirect(url_for('home'))
        

    return render_template('create_acc.html')

# Ml part processing text to predict the personality

@app.route('/predict',methods=['GET','POST'])
@login_required
def classify():
    if request.method=="POST":
        text=str(request.form.get("text"))
        if len(text)>0:
            text=pd.Series(text)
            cleaning(text)
            cv=CountVectorizer(max_features=5000)
            x=cv.fit_transform(text).toarray()
            x=pd.DataFrame(x)
            missing_cols=set(matrix_features.columns)-set(x.columns)
            for i in missing_cols:
                x[i]=0
            pred=model.predict(x)
            key=label_enc.inverse_transform([pred[0]])
            result=trait_provider(key[0])  #trait provider returns the detai of thr key traits given by our model
            usr=Statements(sent=text,user_id=current_user.id,trait=key[0])
            db.session.add(usr)
            db.session.commit()
            return render_template('one.html',text=result,keys=key[0])
    return render_template("one.html")

@app.route('/traits')
@login_required
def traits():
    return render_template("16_traits.html")

@app.route(('/home'))
@login_required
def home():
    return render_template('index.html')

# Logging in the user 

@app.route('/login',methods=['GET','POST'])
def login():
    global users
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('pass')
        users=User.query.filter_by(email=email).first() #checking user in database
        if users:
            if check_password_hash(users.password, password): 

                
                login_user(users,remember=True)
                return redirect(url_for('home'))
            else:

                flash("Password Incorrect",category='error')
        else:

            flash("User does not exist",category='error')       
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__=='__main__':
    #db.create_all() 
    app.run(debug=True)