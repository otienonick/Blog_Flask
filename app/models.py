from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  
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
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    posts = db.relationship('Post',backref = 'user',passive_deletes = True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key = True)
    text = db.Column(db.String,nullable = False)
    date_created = db.Column(db.DateTime(timezone =True),default = func.now())
    author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete = 'CASCADE'),nullable = False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    text = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime(timezone =True),default = func.now())
    author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete = 'CASCADE'),nullable = False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id',ondelete = 'CASCADE'),nullable = False)


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer,primary_key = True)
    author = db.Column(db.Integer,db.ForeignKey('user.id',ondelete = 'CASCADE'),nullable = False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id',ondelete = 'CASCADE'),nullable = False)


   