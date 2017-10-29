from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db ,app
#from app.photos.models import Photo
#from app.albums.models import Album



class Mapp_Albums(db.Model):
    __tablename__ = 'Map_Albums'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    userid=db.Column(db.Integer)
    albumid=db.Column(db.Integer)

    #photos = db.relationship('Photo',backref='person',lazy='dynamic')
    # albums = db.relationship('Album',backref='personalb',lazy='dynamic')
    def __init__(self, userid, albumid):
        self.userid = userid
        self.albumid = albumid

    def to_dict(self):
        return {
            'id' : self.id,
            'userid': self.userid,
            'albumid': self.albumid,
        }

    def __repr__(self):
       # return "User<%d> %s" % (self.id, self.name)
       return "Mapp_Albums { id: %r , userid: %r ,albumid: %r }" (self.id,self.userid,self.albumid)
