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
        try:
            db.session.commit()
        except IntegrityError as e:
            return jsonify(success = False , message= 'This email already exists')

        return jsonify(success = True)

@mod_user.route('/login',methods=['GET','POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success = False, message="%s not entered in the corresponding field" % e.args), 400
    user = User.query.filter(User.email == email).first()
    if user is None or not user.check_password(password):
        return jsonify(success=False, message = "Invalid Credentials"),400
    session['userId'] = user.userId
    return jsonify(success=True)

@mod_user.route('/users', methods= ['GET','POST'])
def get_all_users():
    users = User.query.all()
    return render_template('/user/index.html',users=users)

@mod_user.route('/')
# app.run(debug=True)
