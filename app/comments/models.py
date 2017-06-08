from flask_sqlalchemy import SQLAlchemy
from app import db
'''
class answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    body = db.Column(db.Text)
    roll_no = db.Column(db.Integer)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'))
    complaint = db.relationship('Complaint',backref=db.backref('answers', lazy='dynamic'))
    def __init__(self,body,complaint,roll_no):
        self.body = body
        self.roll_no = roll_no
        self.complaint = complaint
    def __repr__(self):
        return '%r' % self.body
'''
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    username = db.Column(db.String(255))
    userid=db.Column(db.Integer)
    photoid=db.Column(db.Integer)
    text = db.Column(db.Text)
   
    def __init__(self,text,userid,username,photoid):
        self.text = text
        self.userid = userid
        self.photoid=photoid
        self.username=username
    def __repr__(self):
        return '%r' % self.id
