from flask import Blueprint,Flask,render_template,request,redirect,url_for,flash,session,jsonify
from app import db
from app.comment.models import Comment
from app.user.models import User
mod_comment = Blueprint('comment',__name__)
@mod_comment.route('/addComment/<photoid>',methods=['POST'])
def addComment(photoid):
    user = User.query.filter(User.id == session['user_id']).first()
    username =user.name 
    text = request.form['text']
    userid=user.id
    
    comment = Comment(text,userid,username,photoid)
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('mod_user.uploaded_file',fileid = photoid))

'''	
@mod_complaint.route('/addAnswer',methods=['POST'])
def addAnswer():
    roll_no = request.form['roll_no']
    text = request.form['answer_text']
    complaint_id=request.form['complaint_id']
    cobject = Complaint.query.filter_by(id=complaint_id).first()
    answer_new = answer(text,cobject,int(roll_no))
    db.session.add(answer_new)
    db.session.commit()
    return redirect(url_for('mod_stuProfile.view_home',username = roll_no))
'''
