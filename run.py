from app import app
import ssl
from config import Config


#main
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.load_cert_chain(certfile='ssh/simpson.crt',
                            keyfile='ssh/private.key',
                            password='aq1234')
app.run (host='0.0.0.0',
         debug=True,
         ssl_context=ssl_context,
         threaded=True)
