from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import pickle
from flask_login import LoginManager

model = pickle.load(open('website\static\model.pkl','rb'))
matrix_features= pickle.load(open('website\static\matrix_feature.pkl','rb'))
label_enc = pickle.load(open('website\static\label_en.pkl','rb'))

db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.secret_key = "super_secret_key"
    app.config['SQLALCHEMY_DATABASE_URI']= "mysql://root:tool@localhost:3306/personality_clasifier"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)

    from.authentication import authentication
    from.routes import routes

    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(authentication, url_prefix="/")
    
    login_manager = LoginManager()
    login_manager.login_view = 'authentication.login'
    login_manager.init_app(app)
    
    from .db_models import  User,Statements



    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app