import os,time
from flask import *
from sqlalchemy.exc import IntegrityError
from app import db,app
from .models import Mapp_Photos
from app.user.models import User
from werkzeug import secure_filename

mod_mapp = Blueprint('mapp_photo', __name__)

@mod_mapp.route('/photos',methods=['GET','POST'])
def pick_photos():
	print("aa gya")
	user = User.query.filter(User.id == session['user_id']).first()
	print("user mil gya")
	photos=Mapp_Photos.query.filter(Mapp_Photos.userid==user.id).all()
    print("photo")
    return render_template('gallery.html',photos=photos,user=user.to_dict())


'''
can be used as to keep track of the users who have the photo

but as of now no such page is there ,therefore no need of it

@mod_user.route('/<photo_name>',methods=['GET','POST'])
def pick_user():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        return jsonify(success=True, user=user.to_dict())

    return jsonify(success=False), 401
'''

@mod_mapp.route('/<username>/photos/<photo_name>',methods=['GET','POST'])
def display_photo():
    return redirect(url_for('user.uploaded_file',photo_name=photo_name))
    
			
