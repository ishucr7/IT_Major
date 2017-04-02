from flask import *
from sqlalchemy.exc import IntegrityError
from app import db
from .models import User

mod_user = Blueprint('user',__name__)

@mod_user.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            email = request.form['email']
            name = request.form['name']
            userId = request.form['userId']
        except:
            return jsonify(success = False ,message = "please enter all the fields")
        if '@' not in email:
            return jsonify(success = False , message = "Enter a valid email-adress")
        couriers = []
        newUsr = User(userId, email , name, couriers)
        db.session.add(newUsr)
        db.session.commit()
