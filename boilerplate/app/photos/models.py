from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    datetime = db.Column(db.DateTime)
   	likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
   	privacy = db.Column(db.String(255))
    albums=db.relationship('Albums',backref='photo',lazy='dynamic')
    
    def __init__(self, name, date,time,likes,dislikes,privacy):
        self.name = name
        self.datetime=datetime
        self.likes= likes
        self.dislikes=dislikes
        self.privacy=privacy
        
  #  def check_password(self, password):
   #     return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id' : self.id,
            'name': self.name,
        	'datetime': self.datetime,
        	'dislikes': self.dislikes,
        	'likes': self.likes,
        }

    def __repr__(self):
        return "User<%d> %s" % (self.id, self.name)
