import os

from flask import Flask
import jinja2

app = Flask(__name__,static_folder='desticket-static')

app.config.from_pyfile("../settings.cfg")
app.jinja_loader = jinja2.FileSystemLoader([app.config["TEMPLATES_PATH"],
                                          ])


from app import views
