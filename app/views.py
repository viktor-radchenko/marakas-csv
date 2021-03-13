from flask import render_template

from app import app
from app.logger import log


# Normally blueprints are used and views are defined in a seperate module. Routes are put in one file for simplicity
@app.route("/")
def index():
    log(log.INFO, "/ index.html")
    return render_template("index.html")
