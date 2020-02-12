from gevent.pywsgi import WSGIServer
import werkzeug.serving
import logging
from app import app

@werkzeug.serving.run_with_reloader
def runServer():
    app.debug = True
    logging.basicConfig(filename='server.log',level=logging.DEBUG)
    http_server = WSGIServer(('',5000),app)
    http_server.serve_forever()

if __name__=="__main__":
    runServer()
