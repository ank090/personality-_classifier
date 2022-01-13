from flask import Flask, render_template,request,url_for
import pickle
from text_cleaner import cleaning
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from trait_provider import trait_provider

app=Flask(__name__)
model = pickle.load(open('./model.pkl','rb'))
matrix_features= pickle.load(open('./static/matrix_feature.pkl','rb'))
label_enc = pickle.load(open('./static/label_en.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/2',methods=['GET','POST'])
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
            result=trait_provider(key[0])   #trait provider returns the detai of thr key traits given by our model
            return render_template('one.html',text=result,keys=key[0])
    return render_template("one.html")

@app.route('/3')
def traits():
    return render_template("16_traits.html")


if __name__=='__main__':
    app.run(debug=True)
