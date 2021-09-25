from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Quotes:

    '''
    Movie class to define Movie Objects

    '''

    def __init__(self,author,id,quote,permalink):
        self.author = author
        self.id = id
        self.quote = quote
        self.permalink = permalink



class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True,index = True)
    username= db.Column(db.String(150),index = True)
    password =  db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone =True),default = func.now())
    


   