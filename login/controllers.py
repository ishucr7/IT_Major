from flask import *
from sqlalchemy.exc import IntegrityError
from app import db
from .models import User

mod_user = Blueprint('user',__name__)
@mod_user.route('/')
def redir():
    return render_template('index.html')
@mod_user.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            email = request.form['email']
            name = request.form['name']
            password = request.form['password']
            rpassword = request.form['password_confirm']
        except:
            flask.flash('Enter all the fields')
        if '@' not in email:
            flask.flash('enter a valid email')
        if password != rpassword:
            flask.flash('the passwords do not match')
        newUsr = User(email, name, password)
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
        # name = request.form['name']
        password = request.form['password']
    except:
        flask.flash('Enter all the fields')
    user = User.query.filter(User.email == email).first()
    if user is None or not user.check_password(user, password):
        return jsonify(success=False, message = "Invalid Credentials"),400
    session['email'] = user.email
    return jsonify(success=True)

@mod_user.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('email')
    return jsonify(success=True)
