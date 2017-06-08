#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db, app


# from app.photos.models import Photo
# from app.albums.models import Album

class Mapp_Photos(db.Model):

    __tablename__ = 'Map_Photos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    userid = db.Column(db.Integer)
    photoid = db.Column(db.Integer)
    
    liked = db.Column(db.Integer)
    disliked = db.Column(db.Integer)

    # photos = db.relationship('Photo',backref='person',lazy='dynamic')
    # albums = db.relationship('Album',backref='personalb',lazy='dynamic')

    def __init__(self, userid, photoid):
        self.userid = userid
        self.photoid = photoid
        self.liked = 0
        self.disliked = 0

    def likefunc(self):
        self.liked=1
        
    def dislikefunc(self):
        self.disliked=1


    def to_dict(self):
        return {'id': self.id, 'userid': self.userid,
                'photoid': self.photoid}

    def __repr__(self):

       # return "User<%d> %s" % (self.id, self.name)

        return 'Mapp_Photos { id: %r , userid: %r ,photoid: %r }'(self.id,
                self.userid, self.photoid)



			
