"""Haven Domestic Violence Application"""


from jinja2 import StrictUndefined
import datetime
import os
import requests
from flask import Flask, render_template, redirect, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import Question, Form, Answer, Agency, Shelter_Information, Login
from model import Advocate, Victim, Agency_Type, Filled_Form
from model import connect_to_db, db


app = Flask(__name__)

#need app.secret_key if we want to use Flask session and the debug toolbar
app.secret_key = "123"

BACKGROUNDCHECK_APP_ID = os.environ['BACKGROUNDCHECK_APP_ID']
# print BACKGROUNDCHECK_APP_ID
BACKGROUNDCHECK_KEY = os.environ['BACKGROUNDCHECK_KEY']
# print BACKGROUNDCHECK_KEY

#undefined variables in Jinja2 will fail without notifing, so
#StrictUndefined will allow Jinja2 to raise an error for undef variables
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def login():
    """login of domestic violence app"""
 #TODO: for loop (one time), to see see client if advocate or client 

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():
    """login processed """

    #getting login variables
    # import pdb; pdb.set_trace()
    username = request.form['username']
    password = request.form['password']

    user = Login.query.filter_by(user_name=username).first()
    # import pdb; pdb.set_trace()


    if not user:
        flash("Username does not exist")
        return redirect("/")
#TODO: if password correct else: if not correct
    elif user.password != password: #this would be else statment 
        flash("Password incorrect, please try again.")
        return redirect("/")

        #TODO: for loop (one time), to see see client if advocate or client

    session["login_id"] = user.login_id
    #session['victim'] = blah
    #session['advocate'] = blah

    flash("You are logged in")
    return redirect("/welcome")

    #if user.victim == none

    #else
    #advocate
@app.route('/logout')
def logout_process():
    """logout"""
#TODO check ig login id is in session
    del session['login_id']
    flash("Logged Out.")
    return redirect("/")


@app.route('/register', methods=['GET'])
def register_form():
    """User create profile"""

    return render_template("client_or_advocate.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Profile created"""

    client_or_advocate = request.form['advocate/client']

    if client_or_advocate == 'client':
        return redirect("/register/client")

    return redirect("/register/advocate")


@app.route('/register/client', methods=['GET'])
def register_client():
    """Client create profile"""

    all_advocates = Advocate.query.all()

    return render_template("client_registration.html", advocates=all_advocates)


@app.route('/register/client', methods=['POST'])
def client_registration_process():
    """Client create profile"""

    name = request.form['name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    advocate_id = request.form['advocate']

    user = Login(name=name, password=password, user_name=username, email=email)

    advocate = Advocate.query.get(advocate_id)

    new_victim = Victim(login=user, advocate=advocate)
    db.session.add(user)
    db.session.add(new_victim)
    # db.session.add(new_victim)
    db.session.commit()
    flash("You are now registered! Please login.")
    return redirect("/")


@app.route('/register/advocate', methods=['GET'])
def register_advocate():
    """Advocate create profile"""

    shelter_information = Shelter_Information.query.all()

    return render_template("advocate_registration.html",
                            shelter_information=shelter_information)


@app.route('/register/advocate', methods=['POST'])
def advocate_registration_process():
    """Advocate create profile"""

    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    email = request.form['email']
    position_title = request.form['position_title']
    shelter_id = request.form['shelter']

    user = Login(name=name, password=password, user_name=username, email=email)
  

# #drop down menu so when add new shelter informatio will auto populate drop down menu

    shelter_information = Shelter_Information.query.get(shelter_id)
    new_advocate = Advocate(login=user, shelter_information=shelter_information,
                            position_name=position_title)

    db.session.add(user)
    db.session.add(new_advocate)

    db.session.commit()
    flash("You are now registered! Please login.")
    return redirect("/")


@app.route('/welcome')
def homepage():
    """Homepage of domestic violence app"""

    login_id = session.get("login_id")
    victims = Victim.query.all()
    advocates = Advocate.query.all()

    return render_template("homepage.html", login_id=login_id, victims=victims, advocates=advocates)


@app.route('/advocate')
def adocate_view_client_form_names():
    """Advocates view their clients filled out form names"""
    #TODO advocate object -> advocate.victim
    victims = Victim.query.filter_by(advocate_login_id=session["login_id"]).all()

# #       TODO: post route for act of logging in
# # # one time if statement session.get()
    return render_template("advocate_view_forms.html", victims=victims)


@app.route('/advocate/<int:filled_form_id>')
def adocate_view_client_filled_form_content(filled_form_id):
    """Advocates view their clients' questions and answers from filled_forms"""

    filled_form = Filled_Form.query.get(filled_form_id)
    # print filled_form
    
    return render_template("client_forms_qa.html", filled_form=filled_form)



@app.route("/financial")
def financial():
    """Financial Options page: Florida's Victim Compensation form available
        for submitall"""


    question_section_1 = Question.query.filter(Question.section_number == 1, Question.form_id == 2)
    question_section_2 = Question.query.filter(Question.section_number == 2, Question.form_id == 2)
    question_section_3 = Question.query.filter(Question.section_number == 3, Question.form_id == 2)
    question_section_4 = Question.query.filter(Question.section_number == 4, Question.form_id == 2)
    question_section_5 = Question.query.filter(Question.section_number == 5, Question.form_id == 2)

    return render_template("financial_options.html", questions=[question_section_1,
                                                                question_section_2,
                                                                question_section_3,
                                                                question_section_4,
                                                                question_section_5])


@app.route("/financial", methods=["POST"])
def victim_comp_process():
    """"Victim Compensation form is processed"""

    form_id = request.form['form_id']
    form = Form.query.get(form_id)
    victim = Victim.query.get(session["login_id"])
    filled_form = Filled_Form(form=form, victim=victim, time_filled=datetime.datetime.now())
    #working correctly saving filled_form
    db.session.add(filled_form)
    # db.session.commit()

    #list of question object which shows all questions with form_id 2 meaning all questions asociated with 
    # the victim compensation form
    questions_list = filled_form.form.questions
    #looping through the list of question objects
    for question in questions_list:
        # you have a single answer object associated with that question object
        # print question

        # print("Question number: {}".format(question_number))


        key = "section_{}_{}".format(question.section_number, question.question_number)
        # print key
        answer_text = request.form[key]
        # import pdb; pdb.set_trace()
        # print answer_text
    

    #     # for answer in question.answers:
    #     #     answer_form = request.form[answer]
    #     print answer_text
    #         # answer_text = answer.answer_text
        answer_object = Answer(question=question, answer_text=answer_text, filled_form=filled_form)

    #     print answer_object
        db.session.add(answer_object)
    db.session.commit()

    flash("You have successfully submitted your Victim Compensation Application")
    return redirect('/welcome')



# first thing is to get the list of questions, from there associated answer to that question
# then create answer obeject and associate from filled_form amd question object that you are looping through looping over 


    #find out questions need answers form_id to form to questions
    #for each question find answer from the form in the question

    #from html then I am grabbing question number 


@app.route("/safety-plan")
def safety_plan_form():
    """Survivor is able to safety plan and send results directly to police
    department or shelter"""

    question_section_1 = Question.query.filter(Question.section_number == 1, Question.form_id == 1)
    question_section_2 = Question.query.filter(Question.section_number == 2, Question.form_id == 1)
    question_section_3 = Question.query.filter(Question.section_number == 3, Question.form_id == 1)

    return render_template("safety_plan.html", questions=[question_section_1,
                                                          question_section_2,
                                                          question_section_3])


@app.route("/safety-plan", methods=["POST"])
def safety_plan_process():
    """"Safety plan form is processed"""

    form_id = request.form['form_id']
    form = Form.query.get(form_id)
    victim = Victim.query.get(session["login_id"])
    # print request.form.keys()
    # return 'cool'
    filled_form = Filled_Form(form=form, victim=victim, time_filled=datetime.datetime.now())
    # print filled_form
    db.session.add(filled_form)

    question_list = filled_form.form.questions

    for question in question_list:
        key = "section_{}_{}".format(question.section_number, question.question_number)
        answer_text = request.form[key]

        anwer_object = Answer(question=question, answer_text=answer_text, filled_form=filled_form)
        db.session.add(anwer_object)

    db.session.commit()

    flash("You have successfully submitted your safety plan")
    return redirect('/welcome')


@app.route("/shelter")
def shelter():

    """Information about shelter and shelter availability """
#TODO is having a more direct relationship between shelter and advocate shelter.advocate
# if advocate.shelter == shelter
#if true then save boolean variable
    shelter = Shelter_Information.query.first()
    login_id = session.get("login_id")
    advocates = Advocate.query.all()

    return render_template("shelter.html", shelter=shelter, login_id=login_id, advocates=advocates)


@app.route("/shelter", methods=["POST"])
def shelter_process():
    """Update shelter status """

    number_beds = request.form["number_available_beds"]
    next_available_date = request.form["time_available_beds"]

    db.session.query(Shelter_Information).filter(Shelter_Information.shelter_agency_id == 1).update({'next_available_date': next_available_date, 'number_beds': number_beds})
    db.session.commit()

    flash("Shelter status has been changed")
    return redirect("/welcome")


@app.route('/legal')
def legal_advocacy():

    return render_template("legal_advocacy.html")


@app.route('/legal-background', methods=["GET"])
def legal_advocacy_search():
    """Legal Advocacy page: search for offenders with criminal background check
        API."""

    fname = request.args.get('fname')
    lname = request.args.get('lname')
    mname = request.args.get('mname')
    state = request.args.get('state')
    county = request.args.get('county')
    city = request.args.get('city')
    birthyear = request.args.get('birthyear')

    params = {'App_ID': BACKGROUNDCHECK_APP_ID,
                'App_Key': BACKGROUNDCHECK_KEY,
                'Timestamp': datetime.datetime.now(),
                'catalogue': "BACKGROUND",
                'FirstName': fname,
                'LastName': lname,
                'MiddleName': mname,
                'state': state,
                'county': county,
                'city': city,
                'birthyear': birthyear,
                'CrimeType': '',
                'ExactMatch': ""}

    r = requests.get('http://apijson.backgroundcheckapi.com/', params=params)
    # print r.url
    data = r.json()
    # print data['response']

    profile_list_dict = []
    for response in data['response']:
        profile_dict = {}
        # TODO static dictionary key-what i callit, value-what api calls it
        profile_dict["First Name"] = response.get('FirstName', "Not Found")
        profile_dict["Last Name"] = response.get('LastName', "Not Found")
        profile_dict["Date of Birth"] = response.get('DateOfBirth', "Not Found")
        profile_dict["State"] = response.get('State', "Not Found")
        profile_dict["Bond Amount"] = response.get('BondAmount', "Not Found")
        profile_dict["Type"] = response.get('Type', "Not Found")
        profile_dict["Year of Booking"] = response.get('YearOfBooking', "Not Found")
        profile_dict["Entry Date"] = response.get('EntryDate', "Not Found")
        profile_dict["Status"] = response.get('BCType', "Not Found")
        profile_dict["Gender"] = response.get('Gender', "Not Found")
        profile_dict["Age"] = response.get('Age', "Not Found")
        profile_dict["Released Date"] = response.get('ReseasedDate', "Not Found")
        profile_dict["Birth Year"] = response.get('BirthYear', "Not Found")
        profile_dict["Race"] = response.get('Race', "Not Found")
        profile_dict["Booking Date"] = response.get('BookingDate', "Not Found")
        profile_dict["Booking Number"] = response.get('BookingNo', "Not Found")
        profile_dict["Case History"] = response.get('CaseHistory', "Not Found")
        profile_dict["County"] = response.get('County', "Not Found")
        profile_dict["Photo"] = response.get('PHOTO', "Not Found")
        profile_dict["Current Status"] = response.get('CurrentStatus', "Not Found")
        profile_dict["Offence"] = response.get('Offence', "Not Found")
         # print profile

        profile_list_dict.append(profile_dict)

    return render_template("legal_results.html", profile_list_dict=profile_list_dict)



if __name__ == "__main__":

    app.debug = True

    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.config['SQLALCHEMY_ECHO'] = True
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')