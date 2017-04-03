from flask import *
from sqlalchemy.exc import IntegrityError
from app import db
from .models import Security

mod_security = Blueprint('security',__name__,url_prefix='/security')

@mod_security.route('/register', methods=['GET','POST'])
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
        newpersonnel = Security(userId, email , name)
        db.session.add(newpersonnel)
        try:
            db.session.commit()
        except IntegrityError as e:
            return jsonify(success = False , message= 'This email already exists')

        return jsonify(success = True)

@mod_security.route('/login',methods=['GET','POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success = False, message="%s not entered in the corresponding field" % e.args), 400
    personnel = Security.query.filter(Security.email == email).first()
    if personnel is None: #or not personnel.check_password(password):
        return jsonify(success=False, message = "Invalid Credentials"),400
    session['userId'] = personnel.userId
    return jsonify(success=True)

@mod_security.route('/personnels', methods= ['GET','POST'])
def get_all_personnels():
    personnels = Security.query.all()
    return render_template('../templates/security/index.html',personnels=personnels)

@mod_security.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('userId')
    return jsonify(success=True)
