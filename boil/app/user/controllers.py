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
from app.mapp_photos.models import Mapp_Photos

# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded

from werkzeug import secure_filename

mod_user = Blueprint('user', __name__)


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

        # return make_response('Invalid credentials entered')

    session['user_id'] = user.id

    # return jsonify(success=True, user=user.to_dict())
    # return render_template('index.html',user=user.to_dict(),error=error)
    # return render_template('index.html',user=user,error=error)

    return render_template('index.html', user=user.to_dict(),
                           error=error)


@mod_user.route('/logout')
def logout():
    session.pop('user_id')

    # return jsonify(success=True)

    return render_template('login.html')


# from flask import make_response,session

# @mod_user.route('/getVal',methods=['GET'])

# def getValue():
 #   session['x']=request.args.get('val')

    # return make_response(str(session['x']));

# @mod_user.route('/showVal',methods=['GET'])

# def showValue():
 #   if 'x' in session:
  #      return str(session['x'])
   # return "NOt set"

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
    u = User(name, email, password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:

       # return jsonify(success=False, message="This email already exists"), 400

        flash('ther must be some error')

    # return jsonify(success=True)

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

#        uname = user.name
        #tmp = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        tmp = app.config['UPLOAD_FOLDER']+filename
#        if not os.path.exists(tmp):
#            os.makedirs(tmp)
   #     print(user.photoUrl)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo = Photo(filename,"private")
        db.session.add(photo)
        db.session.commit()
        print("photo ban gi")
        mapp_photo = Mapp_Photos(user.id,photo.id)
        print("mapping ho gi")
	db.session.add(mapp_photo)
	db.session.commit()
        return redirect('/photos')






@mod_user.route('/photos', methods=['POST','GET'])
def pick_photos():
    print("aa gya")
    user = User.query.filter(User.id == session['user_id']).first()
    print("user mil gya")
    photos=Mapp_Photos.query.filter(Mapp_Photos.userid==user.id).all()
    
   
    po=[]
    for i in photos:
	o=Photo.query.filter(Photo.id==i.photoid).first()
     	po.append(o)
    print(po)

    if photos is None :
    	print("none")
    return render_template('force.html',photos=po,user=user.to_dict())

        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded fileb
        # return redirect(url_for('bla',filename=filename,user=user))
        #return redirect(url_for('user.uploaded_file',
         #               filename=filename))


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload

@mod_user.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@mod_user.route('/pass_name', methods=['POST', 'GET'])
def aa():
    user = User.query.filter(User.id == session['user_id']).first()

    # return redirect(url_for('static', filename='templates/gallery.html',user=user.to_dict()))

    return render_template('gallery.html', user=user.to_dict())
