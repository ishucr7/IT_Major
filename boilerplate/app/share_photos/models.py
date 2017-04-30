#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from app import db, app
from werkzeug.security import generate_password_hash, \
    check_password_hash
from datetime import datetime

class Share_Photos(db.Model):

    __tablename__ = 'share_photos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    photoid = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    privacy = db.Column(db.String(255))
    sharedby = db.Column(db.String(255))

    def __init__(self,photoid,name,userid,privacy,sharedby):

        self.photoid = photoid
        self.name = name
        self.userid = userid
        self.privacy = privacy
        self.datetime = datetime.now()
        self.likes = 0
        self.dislikes = 0
        self.sharedby = sharedby

    def likefunc(self):
        self.likes =self.likes+1

    def dislikefunc(self):
        self.dislikes =self.dislikes-1

    def to_dictp(self):
        return {
            'id': self.id,
            'photoid':  self.photoid,
            'name': self.name,
            'userid':  self.userid,
            'datetime': self.datetime,
            'dislikes': self.dislikes,
            'likes': self.likes,
            'sharedby': self.sharedby,
            }

    def __repr__(self):
        return 'User<%d> %s' % (self.id, self.name)
