from app import app
import ssl
#main
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.load_cert_chain(certfile='simpson.crt',
                            keyfile='private.key',
                            password='aq1234')
ssl_context_1=('ssh\simpson.crt', 'ssh\private.key')
app.run (host='0.0.0.0',
         debug=True,
         ssl_context=ssl_context,
         threaded=True)
