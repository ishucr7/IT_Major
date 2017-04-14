#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from app import db, app
from werkzeug.security import generate_password_hash, \
    check_password_hash


# from app.photos.models import Photo
# from app.albums.models import Album

class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    # photos = db.relationship('Photo', backref='person', lazy='dynamic')

    # albums = db.relationship('Album',backref='personalb',lazy='dynamic')

    def __init__(
        self,
        name,
        email,
        password,
        ):

        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

    def uName(self):
        return self.name

    def __repr__(self):
        return 'User<%d> %s' % (self.id, self.name)



			
