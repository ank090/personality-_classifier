from flask import render_template,request,flash,url_for,redirect,Blueprint
from .db_models import User,Statements
from.import db
import pickle
from .text_cleaner import cleaning
from . import model,matrix_features,label_enc
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from .trait_provider import trait_provider
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,login_required,current_user
from  werkzeug.security import generate_password_hash,check_password_hash
from sklearn.feature_extraction.text import CountVectorizer

routes=Blueprint("routes",__name__,static_folder="static",template_folder="templates")

# Ml part processing text to predict the personality

@routes.route('/predict',methods=['GET','POST'])
@login_required
def classify():
    if request.method=="POST":
        text1=str(request.form.get("text"))
        if len(text1)>0:
            text=pd.Series(text1)
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
            statement_check = Statements.query.filter_by(sent=text1).first()
            if statement_check:
                return render_template('one.html',text=result,keys=key[0],user=current_user.user_name )
            else:
                usr=Statements(sent=text1,user_id=current_user.id,trait=key[0])
                db.session.add(usr)
                db.session.commit()
                return render_template('one.html',text=result,keys=key[0],user=current_user.user_name )
            
    return render_template("one.html",user=current_user.user_name)

@routes.route('/traits')
@login_required
def traits():
    return render_template("16_traits.html",user=current_user.user_name)

@routes.route(('/home'))
@login_required
def home():
    return render_template('index.html',user=current_user.user_name)

@routes.route("/dashboard",methods=['GET','POST'])
@login_required
def dashboard():
    sentences=Statements.query.filter_by(user_id=current_user.id).all()
    #
    return render_template("dashboard.html",user=current_user.user_name,texts=sentences)


