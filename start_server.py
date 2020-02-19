from app import app

if __name__=="__main__":
    from gevent.pywsgi import WSGIServer
    import werkzeug.serving
    @werkzeug.serving.run_with_reloader
    def runServer():
        app.debug = True
        http_server = WSGIServer(('',5000),app)
        http_server.serve_forever()

    runServer()
