from app import app
from flask_cors import CORS
CORS(app)
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('nginx.key')
context.use_certificate_file('nginx.crt')
app.run(host='0.0.0.0', port=8000, ssl_context=context, threaded=True, debug=True)

