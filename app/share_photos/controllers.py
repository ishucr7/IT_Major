import os,time
from flask import *
from sqlalchemy.exc import IntegrityError
from app import app,db
from .models import Share_Photos

from werkzeug import secure_filename

mod_sharephotos = Blueprint('share_photos',__name__)
'''
@mod_sharephotos.route('/photos/<userid>')
def userphotos(userid):
    user = User.query.filter(User.id == userid).first()


@mod_sharephotos
'''
