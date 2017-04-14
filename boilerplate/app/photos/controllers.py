import os,time
from flask import *
from sqlalchemy.exc import IntegrityError
from app import app,db
from .models import Photos

from werkzeug import secure_filename

mod_photos = Blueprint('photos',__name__)
'''
@mod_photos.route('/photos/<userid>')
def userphotos(userid):
    user = User.query.filter(User.id == userid).first()


@mod_photos
'''