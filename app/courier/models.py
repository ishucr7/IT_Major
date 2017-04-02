from flask import SQLAlchemy
from app import db

class Courier(db.Model):
	__tablename__='courier'
	entry = db.Column(db.Integer, primary_key=True, autoincrement=True)
	courierId = db.Column(db.Integer, primary_key=True, unique=True)
	date = db.Column(db.DATE)
	time = db.Column(db.TIME)
	taken = db.Column(db.Integer)
	sender = db.Column(db.String(100))
	address = db.Column(db.String(100))
	recName = db.Column(db.String(100))
	ctype = db.Column(db.String(20))
	#hostel = db.Column(db.String(20))

	def __init__(self, courierId, date, time, taken, sender, address, recName, ctype):
		self.courierId = courierId
		self.date = date
		self.time = time
		self.taken = taken
		self.sender = sender
		self.address = address
		self.recName = recName
		self.ctype = ctype

	def serialize(self):
		return {'courierId'	:	self.courierId,
				'date'		:	self.date,
				'time'		:	self.time,
				'taken'		:	self.taken,
				'sender'	:	self.sender,
				'address'	:	self.address,
				'recName'	:	self.recName,
				'ctype'		:	self.ctype}