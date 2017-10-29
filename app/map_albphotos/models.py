from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db ,app
#from app.photos.models import Photo
#from app.albums.models import Album



class Mapp_Albphoto(db.Model):
    __tablename__ = 'Map_Albphoto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    photoid=db.Column(db.Integer)
    albumid=db.Column(db.Integer)

    #photos = db.relationship('Photo',backref='person',lazy='dynamic')
    # albums = db.relationship('Album',backref='personalb',lazy='dynamic')
    def __init__(self, albumid, photoid):
        self.photoid = photoid
        self.albumid = albumid

    def to_dict(self):
        return {
            'id' : self.id,
            'photoid': self.photoid,
            'albumid': self.albumid,
        }

    def __repr__(self):
       # return "User<%d> %s" % (self.id, self.name)
       return "Mapp_Albums { id: %r , photoid: %r ,albumid: %r }" (self.id,self.photoid,self.albumid)
