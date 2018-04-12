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
    safety_plan_form = Form(form_name="Safety Plan")

    # A "Yes" response to any of Questions #1-3 automatically triggers the protocol referral.
    question_1 = Question(
        question_text="Has he/she ever used a weapon against you/threatened you with a weapon",
        question_number=1,
        section_number=1,
        answer_required=True,
        form=safety_plan_form)

    question_2 = Question(
        question_text="Has he/she threatened to kill you or your children?",
        question_number=2,
        section_number=1,
        answer_required=True,
        form=safety_plan_form)

    question_3 = Question(
        question_text="Do you think he/she might try to kill you?",
        question_number=3,
        section_number=2,
        answer_required=True,
        form=safety_plan_form)



    # Negative responses to Questions #1-3, but positive responses to at least four of Questions #4-11,
    #trigger the protocol referral.
    question_4 = Question(question_text="""Does he/she have a gun or can he/she 
                                           get one easily?""",
                          question_number=4,
                          section_number=2,
                          answer_required=True,
                          form=safety_plan_form)

    question_5 = Question(question_text="Has he/she ever tried to choke you?",
                          question_number=5,
                          section_number=3,
                          answer_required=True,
                          form=safety_plan_form)

    question_6 = Question(question_text="""Is he/she violently or constantly
                                    jealous or does he/she control most of your
                                    daily activities?""",
                          question_number=6,
                          section_number=3,
                          answer_required=True,
                          form=safety_plan_form)

    question_7 = Question(question_text="""Have you left him/her or separated 
                                        after living together or being married?""",
                          question_number=7,
                          section_number=4,
                          answer_required=True,
                          form=safety_plan_form)
     question_8 = Question(question_text="Is he/she unemployed?",
                          question_number=8,
                          section_number=4,
                          answer_required=True,
                          form=safety_plan_form)
      question_9 = Question(question_text="Has he/she ever tried to kill himself/herself?",
                            question_number=9,
                            section_number=5,
                            answer_required=True,
                            form=safety_plan_form)
       question_10 = Question(question_text="Do you have a child that he/she knows is not his/hers?",
                             question_number=10,
                             section_number=5,
                             answer_required=True,
                             form=safety_plan_form)
        question_11 = Question(question_text="""Does he/she follow or spy on 
                                            you or leave threatening message?""",
                               question_number=11,
                               section_number=6,
                               answer_required=True,
                               form=safety_plan_form)
        question_12 = Question(question_text="""Is there anything else that worries 
                                            you about your safety? (If 'yes')
                                            What worries you?""",
                             question_number=12,
                             section_number=6,
                             answer_required=True
                             form=safety_plan_form)






    # #creating login for a victim and for an advocate
    login_1 = Login(user_name='advocate_1', password='advocate1234', 
                    email='advocatem@gmail.com', name='Denise')

    login_2 = Login(user_name='victim_1', password='victim1234', 
                    email='victim@gmail.com', name='Lauren')

    # #creating agency type
    agency_type_1= Agency_Type(agency_type="Domestic Violence Center")

    # #creating agency
    agency_1 = Agency(agency_name="The Haven", 
                        agency_address='1412 North Fort Harrison Clearwater Fl',
                        agency_phone=7274424128, agency_type=agency_type_1)

    # #creating shelter
    s1 = 'Monday, February 01, 2018'
    shelter_information_1 = Shelter_Information(agency=agency_1, number_beds=42, 
                                                next_available_date=datetime.strptime(s1, "%A, %B %d, %Y"),
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
    answer_2 = Answer(question=question_2, answer_text="Answer text 2", 
                        filled_form=filled_form_1)
    answer_3 = Answer(question=question_3, answer_text="Answer text 3",
                        filled_form=filled_form_1)
    answer_4 = Answer(question=question_4, answer_text="Answer text 4", 
                        filled_form=filled_form_1)

    #addcing to objects to session
    db.session.add_all([form_1, question_1, question_2, question_3, question_4, 
                        login_1, login_2, agency_type_1,
                        agency_1, shelter_information_1, 
                        advocate_1, victim_1, filled_form_1, answer_1, 
                        answer_2, answer_3, answer_4])
                        
                

    #commiting objects
    db.session.commit()




##############################################################################
if __name__ == "__main__":
    connect_to_db(app)

    #Creating tables
    db.create_all()

    #importing data
    seed_data()

