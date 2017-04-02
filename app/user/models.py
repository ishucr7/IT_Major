from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
	__tablename__='user'
	userId = db.column(db.Integer,primary_key=True)
	email = db.column(db.String(80))
	name = db.column(db.String(80))

	def __init__(self, userId, email, name):
		self.userId = userId
		self.email = email
		self.name = name

	def __repr__(self):
		return "User { ID: %r, Email: %r, Name: %r}" %(self.userId, self.email, self.name)
