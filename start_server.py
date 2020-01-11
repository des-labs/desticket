from gevent.pywsgi import WSGIServer
from app import app
import logging

if __name__=="__main__":
    logging.basicConfig(filename='server.log',level=logging.DEBUG)
    http_server = WSGIServer(('',5000),app)
    http_server.serve_forever()
