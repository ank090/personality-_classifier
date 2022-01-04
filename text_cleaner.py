import pandas as pd
import re

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import pickle
import nltk
from nltk.corpus import stopwords

"""importing data"""

data=pd.read_csv("mbti_1.csv")
data_processing=data['posts']
y=data.drop('posts',axis='columns')
y.value_counts()

dat=["i am being ridiculous"]
dat=pd.Series(dat)



"""cleaning data """

def cleaning(data):
  clean_data=[]
  lm=WordNetLemmatizer()
  for i in range(len(data)):
    text=re.sub(r"[|,'@$&!*;\"]"," ",data[i])
    text=re.sub(r'http ://([^\s]+)',' ',text)
    text=re.sub(r'http://([^\s]+)',' ',text)
    text=re.sub(r'https://([^\s]+)',' ',text)
    text=re.sub(r"['-:,'_?./%?0-9(),]"," ",text)
    text=text.lower()
    text=text.split()
    for word in text:
      word=lm.lemmatize(word)
    text=list(set(text)-set(stopwords.words('english')))
    text=" ".join(text)
    clean_data.append(text)
  return clean_data
