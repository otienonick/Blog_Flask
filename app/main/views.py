from flask import render_template,abort,redirect,url_for,request,flash
from . import main
from ..requests import get_quote
from .forms import  UpdateProfile
from .. import db,photos
from ..models import User,Post
from flask_login import current_user


@main.route("/")
def index():
    quotes = get_quote()
    posts = Post.query.all()

    return render_template("index.html",  quotes=quotes,user = current_user,posts = posts)


    

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods = ['POST'])
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname = uname))


@main.route('/create_blog',methods = ['GET','POST'])
def create_blog():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash('Blog section cannot be empty',category='error' )
        elif len(text) < 5:
            flash('Content  is too short', category='error')    
        else:
            post = Post(text = text,author =current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created',category='success')  
            return redirect(url_for('main.index'))  

    return render_template('create_blog.html',user = current_user)        

    







