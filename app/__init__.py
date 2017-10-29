# Import flask and template operators
from flask import *
import random 
import string
import os
from flask_recaptcha import ReCaptcha
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from functools import wraps
# Define the WSGI application object
app = Flask(__name__)
recaptcha = ReCaptcha(app=app)
# Configurations
app.config.from_object('config')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfjSR8UAAAAAKZsyFVl1j29Zx058-ktmjtL2_6t'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfjSR8UAAAAAGAstMkLXtNbh6WmZ05KTRZu0h3O'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR,'app/static/uploads')
app.config['UPLOAD_FOLDER_PP'] = os.path.join(BASE_DIR,'app/static/uploads/profile_pics')
app.config['ALLOWED_EXTENSIONS'] = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])


# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) 
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

class DEFAULTS(object):
    IS_ENABLED = True
    THEME = "light"
    TYPE = "image"
    SIZE = "normal"
    TABINDEX = 0


class ReCaptcha(object):

    VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
    site_key = None
    secret_key = None
    is_enabled = False

    def __init__(self, app=None, site_key=None, secret_key=None, is_enabled=True, **kwargs):
        if site_key:
            self.site_key = site_key
            self.secret_key = secret_key
            self.is_enabled = is_enabled
            self.theme = kwargs.get('theme', DEFAULTS.THEME)
            self.type = kwargs.get('type', DEFAULTS.TYPE)
            self.size = kwargs.get('size', DEFAULTS.SIZE)
            self.tabindex = kwargs.get('tabindex', DEFAULTS.TABINDEX)

        elif app:
            self.init_app(app=app)

    def init_app(self, app=None):
        self.__init__(site_key=app.config.get("RECAPTCHA_SITE_KEY"),
                      secret_key=app.config.get("RECAPTCHA_SECRET_KEY"),
                      is_enabled=app.config.get("RECAPTCHA_ENABLED", DEFAULTS.IS_ENABLED),
                      theme=app.config.get("RECAPTCHA_THEME", DEFAULTS.THEME),
                      type=app.config.get("RECAPTCHA_TYPE", DEFAULTS.TYPE),
                      size=app.config.get("RECAPTCHA_SIZE", DEFAULTS.SIZE),
                      tabindex=app.config.get("RECAPTCHA_TABINDEX", DEFAULTS.TABINDEX))

        @app.context_processor
        def get_code():
            return dict(recaptcha=Markup(self.get_code()))

    def get_code(self):
        """
        Returns the new ReCaptcha code
        :return:
        """
        return "" if not self.is_enabled else ("""
        <script src='//www.google.com/recaptcha/api.js'></script>
        <div class="g-recaptcha" data-sitekey="{SITE_KEY}" data-theme="{THEME}" data-type="{TYPE}" data-size="{SIZE}"\
         data-tabindex="{TABINDEX}"></div>
        """.format(SITE_KEY=self.site_key, THEME=self.theme, TYPE=self.type, SIZE=self.size, TABINDEX=self.tabindex))

    def verify(self, response=None, remote_ip=None):
        if self.is_enabled:
            data = {
                "secret": self.secret_key,
                "response": response or request.form.get('g-recaptcha-response'),
                "remoteip": remote_ip or request.environ.get('REMOTE_ADDR')
            }

            r = requests.get(self.VERIFY_URL, params=data)
            return r.json()["success"] if r.status_code == 200 else False
        return True

from app.user.models import User
from app.photos.models import Photo
from app.albums.models import Album
from app.mapp_photos.models import Mapp_Photos
from app.share_photos.models import Share_Photos

# Sample HTTP error handling
# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
   return render_template('index.html'), 200

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(message="Unauthorized", success=False), 401
        return f(*args, **kwargs)
    return decorated

# Import a module / component using its blueprint handler variable (mod_auth)
from app.user.controllers import mod_user
#from app.todo.controllers import mod_todo

# Register blueprint(s)
app.register_blueprint(mod_user)
#app.register_blueprint(mod_todo)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()









































# Import flask and template operators
from flask import *

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from functools import wraps
# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/home/aashish/ITWS-2/IT____MAJOR/it_mm/boilerplate/app/static/uploads/'
app.config['UPLOAD_FOLDER_PP'] = '/home/aashish/ITWS-2/IT____MAJOR/it_mm/boilerplate/app/static/uploads/profile_pics'
app.config['ALLOWED_EXTENSIONS'] = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

from app.user.models import User
from app.photos.models import Photo
from app.albums.models import Album
from app.mapp_photos.models import Mapp_Photos
from app.share_photos.models import Share_Photos

# Sample HTTP error handling
# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
   return render_template('index.html'), 200

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(message="Unauthorized", success=False), 401
        return f(*args, **kwargs)
    return decorated

# Import a module / component using its blueprint handler variable (mod_auth)
from app.user.controllers import mod_user
#from app.todo.controllers import mod_todo

# Register blueprint(s)
app.register_blueprint(mod_user)
#app.register_blueprint(mod_todo)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
