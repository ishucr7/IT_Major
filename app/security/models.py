from flask_sqlalchemy import SQLAlchemy
from app import db

class Security(db.Model):
    __tablename__= 'security'
    entry = db.Column(db.Integer, primary_key=True, autoincrement= True)
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    name = db.Column(db.String(40))

    def __init__(self,userId, email, name):
         self.userId = userId
         self.email = email
         self.name = name
         
    def check_password(self, password):
		return check_password_hash(self.password, password)

    def serialize(self):
        return {'userID':	self.userId,
				'name'	:	self.name,
				'email'	:	self.email}
