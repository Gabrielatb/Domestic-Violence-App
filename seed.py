"""File to seed data from model.py"""

from model import Question, Form, Answer, Agency, Shelter_Information, Login
from model import Advocate, Victim, Agency_Type, Filled_Form
from model import connect_to_db, db

from sqlalchemy import func
#from server import app
from datetime import datetime
##############################################################################

def seed_forms_questions_answers():
    """Seeding questions from Question class into database"""
    
    #see we are under the seed_question function
    print "Now seeing questions, answers and forms"
    
    #creating forms
    form_1 = Form(form_name="Form Name 1")

    #creating questions "
    question_1 = Question(
        question_text="This question 1 text",
        question_number=1,
        section_number=1,
        answered_req=True,
        form=form_1)

    question_2 = Question(
        question_text="This is question 2 text",
        question_number=2,
        section_number=1
        answered_req=True,
        form=form_1)

    question_3 = Question(
        question_text="This is question 3 text",
        question_number=3,
        section_number=2
        answered_req=False,
        form=form_1)

    question_4 = Question(
        question_text="This is question 4 text",
        question_number=4,
        section_number=2
        answered_req=False,
        form=form_1)

    login_1 = Login(user_name='advocate_1', password='advocate1234', email='advocatem@gmail.com', name='Denise')

    login_2 = Login(user_name='victim_1', password='victim1234', email='victim@gmail.com', name='Lauren')

    agency_type_1= Agency_Type(agency_tpe="Domestic Violence Center")

    agency_1 = Agency(agency_name="The Haven", 
                        agency_address='1412 North Fort Harrison Clearwater Fl',
                        agency_phone=7274424128, agency_type=agency_type_1)

    s = 'Monday, February 01, 2018'
    shelter_information_1 = Shelter_Information(number_beds=42, next_available_date= datetime.strptime(p, "%A, %B %d, %Y"),
                                         agency=agency_1, hotline_number=18007997233)

    advocate_1 = Advocate(login=login_1, shelter_information= shelter_information_1, 
                            position_name="Legal Advocate")

    victim_1 = Victim(advocate=advocate_1, login=login_2)

    s = 'Monday, January 01, 2018'
    filled_form_1 = Filled_Form(form=form_1, victim = victim_1 ,
                                         time_filled=datetime.strptime(s, "%A, %B %d, %Y"))

    answer_1 = Answer(question=question_1, answer_text="Answer text 1",
                            filled_form=filled_form_1)
    answer_2 = Answer(question_number=2, answer_text="Answer text 2")
    answer_3 = Answer(question_number=3, answer_text="Answer text 3")
    answer_4 = Answer(question_number=4, answer_text="Answer text 4")

    db.session.add_all([form_1, question_1, question_2, question_3, question_4,
                        login_1, login_2, agency_type_1, agency_1, shelter_information_1, advocate_1,
                        victim_1, filled_form_1, answer_1, answer_2, answer_3, answer_4])

    db.session.commit()




##############################################################################
if __name__ == "__main__":
    connect_to_db(app)

    #Creating tables
    db.create_all()
