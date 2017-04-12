from flask_sqlalchemy import SQLAlchemy
from app import db,app
from werkzeug.security import generate_password_hash, check_password_hash
# from app.user.models import User
#from app.photos.models import Photo

class Album(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    datetime = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    privacy = db.Column(db.String(255))
    photo_id=db.Column(db.Integer,db.ForeignKey('photo.id'))
    # perrsonalb_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, name, datetime,likes,dislikes,privacy,photos):
        self.name = name
        self.datetime=datetime
        self.likes= likes
        self.dislikes=dislikes
        self.privacy=privacy
        self.photos=photos


    def to_dict(self):
        return {
            'id' : self.id,
            'name': self.name,
            'datetime': self.datetime,
        	'dislikes': self.dislikes,
        	'likes': self.likes,
        	'photos': self.photos
        }

    def __repr__(self):
        return "User<%d> %s" % (self.id, self.name)
