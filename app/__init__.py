import os

from flask import Flask
import jinja2
import logging

app = Flask(__name__,static_folder='static')
app.config.from_pyfile("../settings.cfg")
app.jinja_loader = jinja2.FileSystemLoader([app.config["TEMPLATES_PATH"]])
logging.basicConfig(filename='server.log',level=logging.INFO)

from app import views
