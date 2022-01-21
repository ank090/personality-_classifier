from flask import render_template,request,flash,url_for,redirect,Blueprint
from .db_models import User,Statements
from.import db
import pickle
from .text_cleaner import cleaning
from. import model,matrix_feature,label_enc
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from .trait_provider import trait_provider
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,logout_user,login_required,current_user,UserMixin,LoginManager,current_user
from  werkzeug.security import generate_password_hash,check_password_hash
from sklearn.feature_extraction.text import CountVectorizer
from flask import Blueprint


routes=Blueprint("routes",__name__,static_folder="static",template_folder="templates")

#Sign up ---Creating account---


# Ml part processing text to predict the personality

@routes.route('/predict',methods=['GET','POST'])
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

@routes.route('/traits')
@login_required
def traits():
    return render_template("16_traits.html")

@routes.route(('/home'))
@login_required
def home():
    return render_template('index.html')

# Logging in the user 


