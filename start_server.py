from gevent.pywsgi import WSGIServer
from app import app
if __name__=="__main__":
    http_server = WSGIServer(('',5000),app,log=app.logger)
    http_server.serve_forever()

    #app.run(debug=True)
