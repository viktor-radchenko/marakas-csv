import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

from config import config


app = Flask(__name__)
db = SQLAlchemy()

# Set app config.
env = os.environ.get("FLASK_ENV", "development")
app.config.from_object(config[env])
config[env].configure(app)

# Set up extensions.
db.init_app(app)


# Set up error handler page
@app.errorhandler(HTTPException)
def handle_http_error(exc):
    return render_template('error.html', error=exc), exc.code


# Agains pep8 howevere helps avoiding circular imports issue
from . import views  # noqa 402, 401
