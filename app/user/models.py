from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
	__tablename__='user'
	entry = db.Column(db.Integer, primary_key=True, autoincrement=True)
	userId = db.Column(db.Integer, unique=True)
	email = db.Column(db.String(80) , unique =True)
	name = db.Column(db.String(80))
	couriers = db.Column(db.String)
	password = db.Column(db.String)
	def __init__(self, userId, email, name):
		self.userId = userId
		self.email = email
		self.name = name
		self.couriers = []
	def check_password(self, password):
		return check_password_hash(self.password, password)
# <<<<<<< HEAD
# =======
#
#             return check_password_hash(self.password, password)
# >>>>>>> b13f55f1483605fddf0e8ae22087394f50589318

	def serialize(self):
		return {'userID':	self.userId,
				'name'	:	self.name,
				'email'	:	self.email,}
