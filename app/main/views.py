from flask import render_template,abort,redirect,url_for,request,flash,jsonify
from . import main
from ..requests import get_quote
from .forms import  UpdateProfile
from .. import db,photos
from ..models import User,Post,Comment,Like
from flask_login import current_user




@main.route("/")
def index():
    posts = Post.query.all()

    return render_template("index.html", user = current_user,posts = posts)

    

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
    quotes = get_quote()

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

    return render_template('create_blog.html',user = current_user,quotes=quotes)        

    

@main.route('/delete-blog/<id>')
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash('post does not exist!', category='error')
  
    else:    
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted',category='success')

    return redirect(url_for('main.index'))

@main.route('/posts/<username>')
def posts(username):
    user = User.query.filter_by(username = username).first()
    if not user:
        flash('No user with that username exists',category='error')
        return redirect(url_for('views.index'))
    posts = user.posts
    return render_template('single_blog.html',user = current_user,posts = posts,username = username)


@main.route('/create-comment/<post_id>',methods =['POST'])
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty.',category='error')
    else: 
        post = Post.query.filter_by(id = post_id)
        if post:
            comment = Comment(text = text, author = current_user.id , post_id = post_id)
            db.session.add(comment)
            db.session.commit()
            flash('comment was added',category='success')

        else:
            flash('Post does not exist',category='error')    
    return redirect(url_for('main.index'))

@main.route('/delete-comment/<comment_id>')   
def  delete_comment(comment_id):
        comment = Comment.query.filter_by(id =comment_id).first()

        if not comment:
            flash('comment does not exist!', category='error')
  
        else:    
            db.session.delete(comment)
            db.session.commit()
            flash('Comment deleted',category='success')

        return redirect(url_for('main.index'))

@main.route('/like-post/<post_id>',methods = ['POST'])
def like(post_id):
    post =Post.query.filter_by(id = post_id).first()
    like = Like.query.filter_by(author = current_user.id,post_id = post_id).first()
    if not post:
        return jsonify({'error' : 'Post does not exist'},400)
    elif like:
        db.session.delete(like)   
        db.session.commit() 
    else:
        like = Like(author = current_user.id,post_id = post_id)
        db.session.add(like)
        db.session.commit()  

    return jsonify({'likes' : len(post.likes),'liked': current_user.id in map(lambda x:x.author,post.likes)})  #  tell us if the current user has liked the post.     




