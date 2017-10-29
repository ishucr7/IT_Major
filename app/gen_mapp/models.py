#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from app import db, app
from werkzeug.security import generate_password_hash, \
    check_password_hash


# from app.photos.models import Photo
# from app.albums.models import Album

class Gen(db.Model):

    __tablename__ = 'Gen'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photoid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    liked = db.Column(db.Integer)
    disliked = db.Column(db.Integer)

    # photos = db.relationship('Photo', backref='person', lazy='dynamic')

    # albums = db.relationship('Album',backref='personalb',lazy='dynamic')

    def __init__(self,photoid,userid):

        self.photoid = photoid
        self.userid = userid
        self.liked = 0
        self.disliked = 0

   
    def to_dict(self):
        return {'id': self.id, 'photoid': self.photoid, 'userid': self.userid}

    def __repr__(self):
        return 'User<%d>' % (self.id)



			
