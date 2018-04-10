"""Haven Domestic Violence Application"""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import Question, Form, Answer, Agency, Shelter_Information, Login
from model import Advocate, Victim, Agency_Type, Filled_Form
from model import connect_to_db, db


app = Flask(__name__)

app.secret_key = "123"

app.jinja_env.undefined = StrictUndefined


if __name__ == "__main__":

    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.config['SQLALCHEMY_ECHO'] = True
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')