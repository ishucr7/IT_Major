from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
	__tablename__='user'
	entry = db.Column(db.Integer, primary_key=True, autoincrement=True)
	userId = db.Column(db.Integer,primary_key=True, unique=True)
	email = db.Column(db.String(80))
	name = db.Column(db.String(80))
	couriers = db.Column(db.String)

	def __init__(self, userId, email, name):
		self.userId = userId
		self.email = email
		self.name = name
		self.couriers = []

	def serialize(self):
		return {'userID':	self.userId,
				'name'	:	self.name,
				'email'	:	self.email}