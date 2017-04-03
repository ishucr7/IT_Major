from flask import *
from app import app, db
from flask_cors import CORS
CORS(app)

if __name__ == '__main__':
    db.create_all()
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(port=8080, debug=True)
