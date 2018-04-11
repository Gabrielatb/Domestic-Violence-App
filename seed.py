"""File to seed data from model.py"""

from model import Question, Form, Answer, Agency, Shelter_Information, Login
from model import Advocate, Victim, Agency_Type, Filled_Form
from model import connect_to_db, db

from sqlalchemy import func
from server import app
from datetime import datetime
##############################################################################

def seed_data():
    """Seeding questions from Question class into database"""
    
    #see we are under the seed_question function
    print "Seed Complete."
    
    #creating forms
    form_1 = Form(form_name="Form Name 1")

    #creating questions 
    question_1 = Question(
        question_text="This question 1 text",
        question_number=1,
        section_number=1,
        answered_req=True,
        form=form_1)

    question_2 = Question(
        question_text="This is question 2 text",
        question_number=2,
        section_number=1,
        answered_req=True,
        form=form_1)

    question_3 = Question(
        question_text="This is question 3 text",
        question_number=3,
        section_number=2,
        answered_req=False,
        form=form_1)

    question_4 = Question(
        question_text="This is question 4 text",
        question_number=4,
        section_number=2,
        answered_req=False,
        form=form_1)

    # #creating login for a victim and for an advocate
    login_1 = Login(user_name='advocate_1', password='advocate1234', email='advocatem@gmail.com', name='Denise')

    login_2 = Login(user_name='victim_1', password='victim1234', email='victim@gmail.com', name='Lauren')

    # #creating agency type
    agency_type_1= Agency_Type(agency_type="Domestic Violence Center")

    # #creating agency
    agency_1 = Agency(agency_name="The Haven", 
                        agency_address='1412 North Fort Harrison Clearwater Fl',
                        agency_phone=7274424128, agency_type=agency_type_1)

    # #creating shelter
    s1 = 'Monday, February 01, 2018'
    shelter_information_1 = Shelter_Information(agency=agency_1, number_beds=42, next_available_date= datetime.strptime(s1, "%A, %B %d, %Y"),
                                             hotline_number=18007997233)

    # #creating advocate
    advocate_1 = Advocate(login=login_1, shelter_information= shelter_information_1, 
                            position_name="Legal Advocate")
    # #creating victim
    victim_1 = Victim(login=login_2, advocate=advocate_1)

    # #creating filled form
    s2 = 'Monday, January 01, 2018'
    filled_form_1 = Filled_Form(form=form_1, victim=victim_1,
                                         time_filled=datetime.strptime(s2, "%A, %B %d, %Y"))

    # #creating answers
    answer_1 = Answer(question=question_1, answer_text="Answer text 1",
                            filled_form=filled_form_1)
    answer_2 = Answer(question=question_2, answer_text="Answer text 2", filled_form=filled_form_1)
    answer_3 = Answer(question=question_3, answer_text="Answer text 3", filled_form=filled_form_1)
    answer_4 = Answer(question=question_4, answer_text="Answer text 4", filled_form=filled_form_1)

    #addcing to objects to session
    db.session.add_all([form_1, question_1, question_2, question_3, question_4, login_1, login_2, agency_type_1,
                            agency_1, shelter_information_1, advocate_1, victim_1, filled_form_1, answer_1, answer_2, answer_3, answer_4])
                        
                

    #commiting objects
    db.session.commit()




##############################################################################
if __name__ == "__main__":
    connect_to_db(app)

    #Creating tables
    db.create_all()

    #importing data
    seed_data()

