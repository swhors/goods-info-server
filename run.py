from app import app

#main
app.run (host="0.0.0.0", port=5000, debug=True, ssl_context='adhoc')
