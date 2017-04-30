#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from app import db, app
from werkzeug.security import generate_password_hash, \
    check_password_hash
from datetime import datetime

class Photo(db.Model):

    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    userid = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    privacy = db.Column(db.String(255))

    def __init__(self,name,userid,privacy):

        self.name = name
        self.privacy = privacy
        self.userid = userid
        self.datetime = datetime.now()
        self.likes = 0
        self.dislikes = 0

    def likefunc(self):
        self.likes =self.likes+1

    def dislikefunc(self):
        self.dislikes =self.dislikes-1

    def assignurl(ul):
        self.photo_url.append(ul)

    def to_dictp(self):
        return {
            'id': self.id,
            'name': self.name,
            'userid': self.userid,
            'datetime': self.datetime,
            'dislikes': self.dislikes,
            'likes': self.likes,
            }

    def __repr__(self):
        return 'User<%d> %s' % (self.id, self.name)
