    #!/usr/bin/python
    # -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from app import db, app
from werkzeug.security import generate_password_hash, \
    check_password_hash
from datetime import datetime

class Album(db.Model):

    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    datetime = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    privacy = db.Column(db.String(255))
    #photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    #personalb_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    main_photo=db.Column(db.Integer)
    userid = db.Column(db.Integer)
    
    
    def __init__(
        self,
        name,
        userid
        ,main_photo):
        self.name = name
        self.datetime = datetime.now()
        self.likes = 0
        self.dislikes = 0
        self.privacy = "private"
        self.userid=userid
        self.main_photo = main_photo    
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'datetime': self.datetime,
            'dislikes': self.dislikes,
            'likes': self.likes,
            'userid':self.userid
            }
    def __repr__(self):
        return 'User<%d> %s' % (self.id, self.name)
