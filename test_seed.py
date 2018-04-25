"""File to seed data from model.py"""

from model import Question, Form, Answer, Agency, Shelter_Information, Login
from model import Advocate, Victim, Agency_Type, Filled_Form
from model import connect_to_db, db

from sqlalchemy import func
from server import app
from datetime import datetime

##############################################################################

def test_seed_data():
    """Seeding questions from Question class into database"""

    print "Seed Complete."
    #creating forms
    safety_plan_form = Form(form_name="Safety Plan")

    #creating login for a victim and for an advocate
    login_1 = Login(user_name='advocate_1', password='advocate1234',
                    email='advocatem@gmail.com', name='Denise')

    login_2 = Login(user_name='victim_1', password='victim1234',
                    email='victim@gmail.com', name='Lauren')

    #creating agency type
    agency_type_1 = Agency_Type(agency_type="Domestic Violence Center")

    # #creating agency
    agency_1 = Agency(agency_name="The Haven",
                      agency_address='1412 North Fort Harrison Clearwater Fl',
                      agency_phone=7274424128, agency_type=agency_type_1)

    #creating shelter
    s1 = 'Monday, February 01, 2018'
    shelter_information_1 = Shelter_Information(agency=agency_1, number_beds=42,
                                                next_available_date=datetime.strptime(s1, "%A, %B %d, %Y"))

    #creating advocate
    advocate_1 = Advocate(login=login_1, shelter_information=shelter_information_1,
                          position_name="Legal Advocate")
    #creating victim
    victim_1 = Victim(login=login_2, advocate=advocate_1)


    s2 = 'Monday, January 01, 2019'
    safety_plan_filled_form = Filled_Form(form=safety_plan_form, victim=victim_1,
                                          time_filled=datetime.strptime(s2, "%A, %B %d, %Y"))


# ****************************Safety Plan Form**********************************

    # A "Yes" response to any of Questions #1-3 automatically triggers the protocol referral.
    question_1 = Question(question_text="""Has he/she ever used a weapon against
                          you/threatened you with a weapon""",
                          question_number=1,
                          section_number=1,
                          answer_required=True,
                          form=safety_plan_form)

    question_2 = Question(question_text="""Has he/she threatened to
                          kill you or your children?""",
                          question_number=2,
                          section_number=1,
                          answer_required=True,
                          form=safety_plan_form)

    question_3 = Question(question_text="Do you think he/she might try to kill you?",
                          question_number=3,
                          section_number=1,
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
                          section_number=2,
                          answer_required=True,
                          form=safety_plan_form)

    question_6 = Question(question_text="""Is he/she violently or constantly
                                    jealous or does he/she control most of your
                                    daily activities?""",
                          question_number=6,
                          section_number=2,
                          answer_required=True,
                          form=safety_plan_form)

    question_7 = Question(question_text="""Have you left him/her or separated
                          after living together or being married?""",
                          question_number=7,
                          section_number=2,
                          answer_required=True,
                          form=safety_plan_form)
    question_8 = Question(question_text="Is he/she unemployed?",
                          question_number=8,
                          section_number=2,
                          answer_required=True,
                          form=safety_plan_form)
    question_9 = Question(question_text="Has he/she ever tried to kill himself/herself?",
                          question_number=9,
                          section_number=2,
                          answer_required=True,
                          form=safety_plan_form)
    question_10 = Question(question_text="Do you have a child that he/she knows is not his/hers?",
                           question_number=10,
                           section_number=2,
                           answer_required=True,
                           form=safety_plan_form)
    question_11 = Question(question_text="""Does he/she follow or spy on
                            you or leave threatening message?""",
                           question_number=11,
                           section_number=2,
                           answer_required=True,
                           form=safety_plan_form)
    question_12 = Question(question_text="""Is there anything else that worries
                            you about your safety? (If 'yes')
                            What worries you?""",
                           question_number=12,
                           section_number=3,
                           answer_required=True,
                           form=safety_plan_form)


    #creating answers for safety plan filled form
    answer_1 = Answer(question=question_1, answer_text='yes',
                      filled_form=safety_plan_filled_form)
    answer_2 = Answer(question=question_2, answer_text='no',
                      filled_form=safety_plan_filled_form)
    answer_3 = Answer(question=question_3, answer_text='yes',
                      filled_form=safety_plan_filled_form)
    answer_4 = Answer(question=question_4, answer_text='no',
                      filled_form=safety_plan_filled_form)
    answer_5 = Answer(question=question_5, answer_text='yes',
                      filled_form=safety_plan_filled_form)
    answer_6 = Answer(question=question_6, answer_text='no',
                      filled_form=safety_plan_filled_form)
    answer_7 = Answer(question=question_7, answer_text='yes',
                      filled_form=safety_plan_filled_form)
    answer_8 = Answer(question=question_8, answer_text='no',
                      filled_form=safety_plan_filled_form)
    answer_9 = Answer(question=question_9, answer_text='yes',
                      filled_form=safety_plan_filled_form)
    answer_10 = Answer(question=question_10, answer_text='no',
                       filled_form=safety_plan_filled_form)
    answer_11 = Answer(question=question_11, answer_text='yes',
                       filled_form=safety_plan_filled_form)
    answer_12 = Answer(question=question_12, answer_text="Im ok",
                       filled_form=safety_plan_filled_form)

    db.session.add_all([safety_plan_form,
                        #Questions to Safety Plan Form 
                        question_1, question_2, question_3, question_4,
                        question_5, question_6, question_7, question_8,
                        question_9, question_10, question_11, question_12,
                        #Answers to Safety Plan Form 
                        answer_1, answer_2, answer_3, answer_4, answer_5,
                        answer_6, answer_7, answer_8, answer_9, answer_10,
                        answer_11, answer_12, 
                        safety_plan_filled_form,
                        login_1, login_2, agency_type_1,
                        agency_1, shelter_information_1, 
                        advocate_1, victim_1])

# *******************Victim Compensation Form**********************************

    victim_comp_form = Form(form_name="Victim Compensation Application")

    question_1 = Question(question_text="Name: (last, first, middle)",
                          question_number=1,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_2 = Question(question_text="Date of Birth: (MM-DD-YYYY)",
                          question_number=2,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_3 = Question(question_text="E-mail address",
                          question_number=3,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_4 = Question(question_text="Address:",
                          question_number=4,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_5 = Question(question_text="City:",
                          question_number=5,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_6 = Question(question_text="State:",
                          question_number=6,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_7 = Question(question_text="Zipcode:",
                          question_number=7,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_8 = Question(question_text="Telephone Number:",
                          question_number=8,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_9 = Question(question_text="Occupation: (optional)",
                          question_number=9,
                          section_number=1,
                          answer_required=True,
                          form=victim_comp_form)

    question_10 = Question(question_text="Race/Ethnicity:",
                           question_number=10,
                           section_number=1,
                           answer_required=True,
                           form=victim_comp_form)

    question_11 = Question(question_text="Gender:",
                           question_number=11,
                           section_number=1,
                           answer_required=True,
                           form=victim_comp_form)

    question_12 = Question(question_text="National Origin:",
                           question_number=12,
                           section_number=1,
                           answer_required=True,
                           form=victim_comp_form)

    question_13 = Question(question_text="Were you disabled before the crime?:",
                           question_number=13,
                           section_number=1,
                           answer_required=True,
                           form=victim_comp_form)

    question_14 = Question(question_text="Name of person assisting with application (last, first, middle):",
                           question_number=14,
                           section_number=2,
                           answer_required=True,
                           form=victim_comp_form)

    question_15 = Question(question_text="Email address:",
                           question_number=15,
                           section_number=2,
                           answer_required=True,
                           form=victim_comp_form)

    question_16 = Question(question_text="Name of Agency/Organization:",
                           question_number=16,
                           section_number=2,
                           answer_required=True,
                           form=victim_comp_form)

    question_17 = Question(question_text="Agency/Organization's Address: (address, city, state, zip code)",
                           question_number=17,
                           section_number=2,
                           answer_required=True,
                           form=victim_comp_form)

    question_18 = Question(question_text="Telephone Number:",
                           question_number=18,
                           section_number=2,
                           answer_required=True,
                           form=victim_comp_form)

    question_19 = Question(question_text="Is Insurance or Medicaid Available to assist with these expenses?:",
                           question_number=19,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_20 = Question(question_text="Medicaid Number:",
                           question_number=20,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_21 = Question(question_text="Company Name:",
                           question_number=21,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_22 = Question(question_text="Policy Number:",
                           question_number=22,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_23 = Question(question_text="Telephone Number:",
                           question_number=23,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_24 = Question(question_text="Address:",
                           question_number=24,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_25 = Question(question_text="City:",
                           question_number=25,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_26 = Question(question_text="State:",
                           question_number=26,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_27 = Question(question_text="Zipcode:",
                           question_number=27,
                           section_number=3,
                           answer_required=False,
                           form=victim_comp_form)

    question_28 = Question(question_text="Name of Law Enforcement Agency:",
                           question_number=28,
                           section_number=4,
                           answer_required=True,
                           form=victim_comp_form)

    question_29 = Question(question_text="Date of Crime:",
                           question_number=29,
                           section_number=4,
                           answer_required=False,
                           form=victim_comp_form)

    question_30 = Question(question_text="Date Reported To Law Enforcement Agency:",
                           question_number=30,
                           section_number=4,
                           answer_required=False,
                           form=victim_comp_form)

    question_31 = Question(question_text="Was the crime reported to law enforcement within 72 hours?",
                           question_number=31,
                           section_number=4,
                           answer_required=False,
                           form=victim_comp_form)

    question_32 = Question(question_text="""If no, please explain. (If no, failure
                           to provide an acceptable explanation
                           in this section will result in a denial of benefits.""",
                           question_number=32,
                           section_number=4,
                           answer_required=False,
                           form=victim_comp_form)

    question_33 = Question(question_text="""Is the application and and law
                           enforcement report being submitted within one year
                           from the date of crime?""",
                           question_number=33,
                           section_number=4,
                           answer_required=False,
                           form=victim_comp_form)

    question_34 = Question(question_text="""If no, please explain.
                                (Please be advised that most benefi ts apply to
                                treatment losses suffered within one year from
                                the date of crime, with some exceptions for minor victims.
                                If no, failure to provide an acceptable explanation
                                in this section will result in a denial of benefits.)?""",
                           question_number=34,
                           section_number=4,
                           answer_required=False,
                           form=victim_comp_form)

    question_35 = Question(question_text="""Type of crime as specified on the
                           law enforcement report?""",
                           question_number=35,
                           section_number=4,
                           answer_required=True,
                           form=victim_comp_form)

    question_36 = Question(question_text="""Law Enforcement report number""",
                           question_number=36,
                           section_number=4,
                           answer_required=True,
                           form=victim_comp_form)

    question_37 = Question(question_text="""Name of Law Enforcement Officer""",
                           question_number=37,
                           section_number=4,
                           answer_required=True,
                           form=victim_comp_form)

    question_38 = Question(question_text="""Name of offender (if known)""",
                           question_number=38,
                           section_number=4,
                           answer_required=False,
                           form=victim_comp_form)

    question_39 = Question(question_text="""Name of Assistant State Attorney
                                Handling the case (if applicable)""",
                           question_number=39,
                           section_number=4,
                           answer_required=False,
                           form=victim_comp_form)

    question_40 = Question(question_text="""State Attorney/Clerk of Court case
                           Number""",
                           question_number=40,
                           section_number=4,
                           answer_required=True,
                           form=victim_comp_form)
    #Victim Signature
    question_41 = Question(question_text="""Printed Name""",
                           question_number=41,
                           section_number=5,
                           answer_required=True,
                           form=victim_comp_form)

    question_42 = Question(question_text="""Signature""",
                           question_number=42,
                           section_number=5,
                           answer_required=True,
                           form=victim_comp_form)

    question_43 = Question(question_text="""Date""",
                           question_number=43,
                           section_number=5,
                           answer_required=True,
                           form=victim_comp_form)


    # #TO DO: SEE if can use timestamp in order to see the time the form was sent
    # #creating filled victim compensation form
    s2 = 'Monday, January 01, 2018'
    victim_comp_filled_form = Filled_Form(form=victim_comp_form, victim=victim_1,
                                          time_filled=datetime.strptime(s2, "%A, %B %d, %Y"))

    # #creating answers for safety plan filled form
    answer_1 = Answer(question=question_1, answer_text="Gabriela Borges",
                      filled_form=victim_comp_filled_form)
    answer_2 = Answer(question=question_2, answer_text="Answer text 2",
                      filled_form=victim_comp_filled_form)
    answer_3 = Answer(question=question_3, answer_text="Answer text 3",
                      filled_form=victim_comp_filled_form)
    answer_4 = Answer(question=question_4, answer_text="Answer text 4",
                      filled_form=victim_comp_filled_form)
    answer_5 = Answer(question=question_5, answer_text="Answer text 5",
                      filled_form=victim_comp_filled_form)
    answer_6 = Answer(question=question_6, answer_text="Answer text 6",
                      filled_form=victim_comp_filled_form)
    answer_7 = Answer(question=question_7, answer_text="Answer text 7",
                      filled_form=victim_comp_filled_form)
    answer_8 = Answer(question=question_8, answer_text="Answer text 8",
                      filled_form=victim_comp_filled_form)
    answer_9 = Answer(question=question_9, answer_text="Answer text 9",
                      filled_form=victim_comp_filled_form)
    answer_10 = Answer(question=question_10, answer_text="Answer text 10",
                       filled_form=victim_comp_filled_form)
    answer_11 = Answer(question=question_11, answer_text="Answer text 11",
                       filled_form=victim_comp_filled_form)
    answer_12 = Answer(question=question_12, answer_text="Answer text 12",
                       filled_form=victim_comp_filled_form)
    answer_13 = Answer(question=question_13, answer_text="Answer text 13",
                       filled_form=victim_comp_filled_form)
    answer_14 = Answer(question=question_14, answer_text="Answer text 14",
                       filled_form=victim_comp_filled_form)
    answer_15 = Answer(question=question_15, answer_text="Answer text 15",
                       filled_form=victim_comp_filled_form)
    answer_16 = Answer(question=question_16, answer_text="Answer text 16",
                       filled_form=victim_comp_filled_form)
    answer_17 = Answer(question=question_17, answer_text="Answer text 17",
                       filled_form=victim_comp_filled_form)
    answer_18 = Answer(question=question_18, answer_text="Answer text 18",
                       filled_form=victim_comp_filled_form)
    answer_19 = Answer(question=question_19, answer_text="Answer text 19",
                       filled_form=victim_comp_filled_form)
    answer_20 = Answer(question=question_20, answer_text="Answer text 20",
                       filled_form=victim_comp_filled_form)
    answer_21 = Answer(question=question_21, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_22 = Answer(question=question_22, answer_text="Answer text 22",
                       filled_form=victim_comp_filled_form)
    answer_23 = Answer(question=question_23, answer_text="Answer text 23",
                       filled_form=victim_comp_filled_form)
    answer_24 = Answer(question=question_24, answer_text="Answer text 24",
                       filled_form=victim_comp_filled_form)
    answer_25 = Answer(question=question_25, answer_text="Answer text 25",
                       filled_form=victim_comp_filled_form)
    answer_26 = Answer(question=question_26, answer_text="Answer text 26",
                       filled_form=victim_comp_filled_form)
    answer_27 = Answer(question=question_27, answer_text="Answer text 27",
                       filled_form=victim_comp_filled_form)
    answer_28 = Answer(question=question_28, answer_text="Answer text 28",
                       filled_form=victim_comp_filled_form)
    answer_29 = Answer(question=question_29, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_30 = Answer(question=question_30, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_31 = Answer(question=question_31, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_32 = Answer(question=question_32, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_33 = Answer(question=question_33, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_34 = Answer(question=question_34, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_35 = Answer(question=question_35, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_36 = Answer(question=question_36, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_37 = Answer(question=question_37, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_38 = Answer(question=question_38, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_39 = Answer(question=question_39, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_40 = Answer(question=question_40, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_41 = Answer(question=question_41, answer_text="Answer text 21",
                       filled_form=victim_comp_filled_form)
    answer_42 = Answer(question=question_42, answer_text="04/24/2018",
                       filled_form=victim_comp_filled_form)







    # #adding to objects to session
    db.session.add_all([#Questions to Victim Compensation Form 
                        question_1, question_2, question_3, question_4,
                        question_5, question_6, question_7, question_8,
                        question_9, question_10, question_11, question_12,
                        question_13, question_14, question_15, question_16, question_17,
                        question_18, question_19, question_20, question_21, question_22, question_23,
                        question_24, question_25, question_26, question_27, question_28, question_29,
                        question_30, question_31, question_32, question_33, question_34, question_35,
                        question_36, question_37, question_38, question_39, question_40, question_41,
                        question_42, question_43, 
                        #Answers to Victim Compensation Form
                        answer_1, answer_2, answer_3, answer_4, answer_5,
                        answer_6, answer_7, answer_8, answer_9, answer_10,
                        answer_11, answer_12, answer_13, answer_14, answer_15, answer_16, answer_17,
                        answer_18, answer_19, answer_20, answer_21, answer_22,
                        answer_23, answer_24, answer_25, answer_26, answer_27, answer_28, answer_29,
                        answer_30, answer_31, answer_32, answer_33, answer_34,
                        answer_35, answer_36, answer_37, answer_38, answer_39, answer_40, answer_41,
                        answer_6, answer_7, answer_8, answer_9, answer_10,
                        answer_42, victim_comp_form, victim_comp_filled_form])
                            
                        
    #commiting objects
    db.session.commit()




##############################################################################
if __name__ == "__main__":
    connect_to_db(app)

    #Creating tables
    db.create_all()

    #importing data
    test_seed_data()
