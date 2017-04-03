from flask import *
from .models import Courier
from app import db
from sqlalchemy.exc import IntegrityError
import time

mod_courier = Blueprint('courier',__name__,url_prefix='/courier')

@mod_courier.route('/today',methods=['GET','POST'])
def show_todays():
    date=time.strftime("%d/%m/%Y")
    couriers=Courier.query.filter(Courier.date==date).all()
    return render_template("../templates/user/user.html",couriers=couriers)

@mod_courier.route('/couriers',methods=['GET','POST'])
def show_all():
    couriers=Courier.query.all()
    return render_template("../templates/user/all_courier.html",couriers=couriers)
