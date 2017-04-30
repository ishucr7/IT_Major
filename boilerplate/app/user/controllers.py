#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from flask import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from app import db, app
from .models import User
from app.photos.models import Photo
from app.albums.models import Album
from app.mapp_photos.models import Mapp_Photos
from app.map_albphotos.models import Mapp_Albphoto
from app.map_albums.models import Mapp_Albums
from app.comments.models import Comment
from app.share_photos.models import Share_Photos
from app.gen_mapp.models import Gen
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask_recaptcha import ReCaptcha
from werkzeug import secure_filename

mod_user = Blueprint('user', __name__)
recaptcha = ReCaptcha(app=app)
'''
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')
'''
@mod_user.route('/')
def default():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        return render_template('index.html', user=user.to_dict())
    return render_template('login.html')


@mod_user.route('/llo', methods=['GET', 'POST'])
def check_login():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        return jsonify(success=True, user=user.to_dict())

    return (jsonify(success=False), 401)


@mod_user.route('/gall', methods=['GET', 'POST'])
def display_gall():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()

        return render_template('gallery.html', user=user.to_dict())
    return render_template('login.html')


@mod_user.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:

       # return jsonify(success=False, message="%s not sent in the request" % e.args), 400

        error = 'there is some error'
    global user
    user = User.query.filter(User.email == email).first()

    # if user is None or not user.check_password(password):

    if user is None or not user.check_password(password):

        # return jsonify(success=False, message="Invalid Credentials"), 400

        flash('invalid credentials entered')
        return redirect(url_for('user.default'))

    session['user_id'] = user.id

    return render_template('index.html', user=user.to_dict(),
                           error=error)


@mod_user.route('/logout')
def logout():
    session.pop('user_id')

    # return jsonify(success=True)

    return render_template('login.html')


@mod_user.route('/register', methods=['POST'])
def create_user():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        rpassword = request.form['confirm_password']
    except KeyError as e:

       # return jsonify(success=False, message="%s not sent in the request" % e.args), 400

        flash('sorry form error')
    if '@' not in email:

        # return jsonify(success=False, message="Please enter a valid email"), 400

        flash('enter email with @')
    if rpassword != password:

        # return jsonify(success=False, message="Passwords don't match"), 400

        flash('the passwords do not match')
    if recaptcha.verify():
        # SUCCESS
        pass
    else:
        # FAILED
        pass
    u = User(name, email, password)
    db.session.add(u)
    
    

    try:
        db.session.commit()
    except IntegrityError as e:

       # return jsonify(success=False, message="This email already exists"), 400

        flash('ther must be some error')

    # return jsonify(success=True)
    all_photos=Photo.query.all()
    

    for x in all_photos:
        gen=Gen(x.id,u.id)
        db.session.add(gen)
        db.session.commit() 

    return render_template('login.html')


# For a given file, return whether it's an allowed type or not

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] \
        in app.config['ALLOWED_EXTENSIONS']


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation

# Route that will process the file upload

@mod_user.route('/upload', methods=['POST'])
def upload():

    # Get the name of the uploaded file

    file = request.files['file']

    # Check if the file is one of the allowed types/extensions

    if file and allowed_file(file.filename):

        # Make the filename safe, remove unsupported chars

        filename = secure_filename(file.filename)

        # Move the file form the temporal folder to
        # the upload folder we setup

        user = User.query.filter(User.id == session['user_id']).first()


        tmp = app.config['UPLOAD_FOLDER'] + filename

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo = Photo(filename,user.id,'private')
        db.session.add(photo)
        db.session.commit()
        
        all_users=User.query.all()
        for x in all_users :
            gen=Gen(photo.id,x.id)
            db.session.add(gen)
            db.session.commit()

        mapp_photo = Mapp_Photos(user.id, photo.id)
        db.session.add(mapp_photo)
        db.session.commit()
        return redirect('/photos')


@mod_user.route('/photos', methods=['POST', 'GET'])
def pick_photos():
    user = User.query.filter(User.id == session['user_id']).first()
    photos = Mapp_Photos.query.filter(Mapp_Photos.userid
            == user.id).all()
    po = []
    for i in photos:
        o = Photo.query.filter(Photo.id == i.photoid).first()
        po.append(o)

    sh = []
    share = Share_Photos.query.all()
    return render_template('gallery.html', photos=po,shared=share,user=user.to_dict())


        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded fileb
        # return redirect(url_for('bla',filename=filename,user=user))
        # return redirect(url_for('user.uploaded_file',
         #               filename=filename))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@mod_user.route('/sharePhoto/<photoid>', methods=['POST'])
def sharePhoto(photoid):
    user = User.query.filter(User.id == session['user_id']).first()
    username = user.name
    photo = Photo.query.filter(Photo.id == photoid).first()
    photoname = photo.name
    photo.privacy = "Public"

    shared = Share_Photos(photoid,photoname,user.id,"Public",username)
    db.session.add(shared)
    db.session.commit()
    flash("Photo shared successfully")
    return redirect('/photos')

@mod_user.route('/addComment/<photoid>', methods=['POST'])
def addComment(photoid):
    user = User.query.filter(User.id == session['user_id']).first()
    username = user.name
    text = request.form['text']
    userid = user.id

    comment = Comment(text, userid, username, photoid)
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('user.uploaded_file', fileid=photoid))


@mod_user.route('/display/<fileid>')
def uploaded_file(fileid):
    user = User.query.filter(User.id == session['user_id']).first()
    photo = Photo.query.filter(Photo.id == fileid).first()
    comment = Comment.query.filter(photo.id == Comment.photoid)

    return render_template('like.html', user=user.to_dict(),
                           photo=photo, comments=comment)



@mod_user.route('/increment/<photoid>')
def aa(photoid):
    user = User.query.filter(User.id == session['user_id']).first()


    photo = Photo.query.filter(Photo.id == photoid).first()
    g=Gen.query.filter(Gen.photoid==photo.id).all()

    i=0
    for k in range(0,len(g)):
        if g[k].userid==user.id:
            i=k
            break
    if g[i].liked == 0:
        photo.likefunc()
        g[i].liked=1
        db.session.commit()

    
    return redirect(url_for('user.uploaded_file', fileid=photo.id))



@mod_user.route('/decrement/<photoid>')
def da(photoid):
    user = User.query.filter(User.id == session['user_id']).first()


    photo = Photo.query.filter(Photo.id == photoid).first()
    g=Gen.query.filter(Gen.photoid==photo.id).all()

    i=0
    for k in range(0,len(g)):
        if g[k].userid==user.id:
            i=k
            break
    if g[i].disliked == 0:
        photo.dislikefunc()
        g[i].disliked=1
        db.session.commit()
    return redirect(url_for('user.uploaded_file', fileid=photo.id))


@mod_user.route('/deletePhoto/<photoid>',methods = ['POST','GET'])
def dele(photoid):
    photo = Photo.query.filter(Photo.id == photoid).all()
    comment = Comment.query.filter(Comment.photoid == photoid).all()
    mapp = Mapp_Photos.query.filter(Mapp_Photos.photoid == photoid).all()
    share = Share_Photos.query.filter(Share_Photos.photoid == photoid).all()
    user = User.query.filter(User.id == session['user_id']).first()
    for i in photo:
        if i.userid == user.id:
            db.session.delete(i)
    for i in comment:
        if i.userid == user.id:
            db.session.delete(i)
    for i in mapp:
        if i.userid == user.id:
            db.session.delete(i)
    for i in share:
        if i.userid == user.id:
            db.session.delete(i)
    db.session.commit()
    return redirect('/photos')




@mod_user.route('/upload_pp', methods=['POST'])
def uploadpp():
    file = request.files['file']
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        user = User.query.filter(User.id == session['user_id']).first()

        tmp = app.config['UPLOAD_FOLDER_PP'] + filename

        file.save(os.path.join(app.config['UPLOAD_FOLDER_PP'], filename))
        user.dp=filename
        db.session.commit()
        return redirect('/photos')

@mod_user.route('/btw', methods=['POST','GET'])
def btw():
    user = User.query.filter(User.id == session['user_id']).first()
    return render_template("upload.html",user=user.to_dict())


@mod_user.route('/albums',methods=['POST','GET'])
def al():
    user = User.query.filter(User.id == session['user_id']).first()
    photos = Photo.query.filter(Photo.userid==session['user_id'])
    
    return render_template('album.html',photos = photos,user=user)


@mod_user.route('/dont', methods=['POST','GET'])
def aaaa():
    albumname = request.form['album_name']
    pho=request.form['hidden']
    p=pho.split(" ")
    user = User.query.filter(User.id == session['user_id']).first()
    photo = Photo.query.filter(Photo.id==p[0]).first()
    album = Album(albumname,user.id,photo.name)
    
    db.session.add(album)
    db.session.commit()
    
    for i in p:
        mapp_albp = Mapp_Albphoto(album.id,i)
        db.session.add(mapp_albp)
        db.session.commit()
    
    db.session.commit()
    
    return redirect('/albumpage')

@mod_user.route('/albumpage', methods=['POST','GET'])
def llaa():
    albs=Album.query.filter(Album.userid==session['user_id']).all()

    return render_template('slide.html',albums=albs)
    


@mod_user.route('/dispalbum/<albumid>', methods=['POST','GET'])
def ala(albumid):
    album=Album.query.filter(Album.id==albumid).first()
    user = User.query.filter(User.id == session['user_id']).first()
    alb=Mapp_Albphoto.query.filter(albumid==Mapp_Albphoto.albumid).all()
    po=[]
    for i in alb:
        o = Photo.query.filter(Photo.id==i.photoid).first()
        po.append(o)
    return render_template('show.html',photos=po,user=user,album=album)


