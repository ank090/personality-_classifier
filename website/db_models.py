from .import db
from flask_login import UserMixin






class User(db.Model,UserMixin):
         id=db.Column('user_id',db.Integer,primary_key=True)
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