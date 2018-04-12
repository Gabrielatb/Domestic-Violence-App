"""Haven Domestic Violence Application"""


from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, session)
from flask_debugtoolbar import DebugToolbarExtension
from model import Question, Form, Answer, Agency, Shelter_Information, Login
from model import Advocate, Victim, Agency_Type, Filled_Form
from model import connect_to_db, db


app = Flask(__name__)

#need app.secret_key if we want to use Flask session and the debug toolbar
app.secret_key = "123"

# BACKGROUNDCHECK_TOKEN = os.environ.get('BACKGROUNDCHECK_APP_ID')

# #api request endpoint
# BACKGROUNDCHECK_URL = 'http://apijson.backgroundcheckapi.com/'


#undefined variables in Jinja2 will fail without notifing, so 
#StrictUndefined will allow Jinja2 to raise an error for undef variables
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """Homepage of domestic violence app"""

    return render_template("homepage.html")

@app.route('/legal')
def legal_advocacy():
    """Legal Advocacy page: search for offenders with criminal background check
        API."""

        #get request
        
#         payload = {http://apijson.backgroundcheckapi.com/?App_ID=":"[BACKGROUND CHECK API APP
# ID]&App_Key=[BACKGROUND CHECK API APP KEY]&Timestamp=[CURRENT
# TIMESTAMP]&IP=[IP]&catalogue=BACKGROOUND&FirstName= Neal Anderson &LastName= Stanford
# &MiddleName=&State= Washington &County= Benton &City= STEILACOOM
# &BirthYear=&CrimeType=&ExactMatch=Yes}



#         http://apijson.backgroundcheckapi.com/?App_ID=":"[BACKGROUND CHECK API APP
# ID]&App_Key=[BACKGROUND CHECK API APP KEY]&Timestamp=[CURRENT
# TIMESTAMP]&IP=[IP]&catalogue=BACKGROOUND&FirstName= Neal Anderson &LastName= Stanford
# &MiddleName=&State= Washington &County= Benton &City= STEILACOOM
# &BirthYear=&CrimeType=&ExactMatch=Yes


    return render_template("legal_advocacy.html")

@app.route("/financial")
def financial():
    """Financial Options page: Florida's Victim Compensation form available
        for submitall"""

    return render_template("financial_options.html")

@app.route("/shelter")
def shelter():
    """Information about shelter and shelter availability """

    return render_template("shelter.html")


@app.route("/safety-plan")
def safety_plan():
    """Survivor is able to safety plan and send results directly to police
    department or shelter"""

    question = Question.query.all()
    return render_template("safety_plan.html", question=question)



if __name__ == "__main__":

    app.debug = True

    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    app.config['SQLALCHEMY_ECHO'] = True
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')