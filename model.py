"""Models and database functions."""

#Using Flask-SQLAlchemy library
from flask_sqlalchemy import SQLAlchemy
#Using datetime library 
import datetime

db = SQLAlchemy()

##############################################################################


#Model definitions


class Question(db.Model):
    """Questions for each form """


    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_id = db.Column(db.Integer,
                        db.ForeignKey('forms.form_id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    section_number = db.Column(db.Integer, nullable=False)
    answer_required = db.Column(db.Boolean, default=True, nullable=False)

    form = db.relationship("Form",
                           backref=db.backref("questions"))



    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Question ID: {}, Form ID: {}, Question Text: {}, 
            Question_Number: {}, Section Number: {} Answer Required: {}>""".format(
                                self.question_id, self.form_id, self.question_text,
                                self.question_number, self.section_number, self.answer_required)


class Form(db.Model):
    """Form type"""


    __tablename__ = "forms"

    form_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    form_name = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Form ID: {}, Form Name: {}>".format(self.form_id,
                                               self.form_name)


class Answer(db.Model):
    """Answer to questions within form"""

    __tablename__ = "answers"

    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer,
                         db.ForeignKey('questions.question_id'))
    answer_text = db.Column(db.String(500), nullable=True)

    filled_form_id = db.Column(db.Integer, db.ForeignKey('filled_forms.filled_form_id'))

    #Define relationship to Question
    question = db.relationship("Question",
                               backref=db.backref("answers"))

    filled_form = db.relationship("Filled_Form",
                                  backref=db.backref("answers"))
    
                                             

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Answer ID: {}, Question ID: {}, Answer Text: {}, >".format(
                                                                        self.answer_id,
                                                                        self.question_id,
                                                                        self.answer_text)

class Agency(db.Model):
    """Agency information, specification"""


    __tablename__ = "agencies"

    agency_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agency_name = db.Column(db.String(100), nullable=False)
    agency_address = db.Column(db.String(500), nullable=False)
    agency_phone = db.Column(db.BigInteger, nullable=False)
    agency_type_id = db.Column(db.Integer,
                                    db.ForeignKey('agency_type.agency_type_id'))

    # Define relationship to Agency_Type
    agency_type = db.relationship("Agency_Type",
                           backref=db.backref("agency"))
                                              


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Agency ID {}, Agency Name {}>".format(self.agency_id,
                                                self.agency_name)


class Shelter_Information(db.Model):
    """Shelter information connected to one domestic violence agency """

    __tablename__ = "shelter_information"

    shelter_agency_id = db.Column(db.Integer, db.ForeignKey('agencies.agency_id'),
                                  primary_key=True)
    number_beds = db.Column(db.Integer, nullable=False)
    next_available_date = db.Column(db.DateTime, nullable=True)

    # Define relationship to Agency
    agency = db.relationship("Agency",
                             backref=db.backref("shelter_information"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Shelter Agency Id: {}, Number of Beds: {}, Next Available Date: {}>".format(
                                            self.shelter_agency_id, self.number_beds, self.next_available_date)

class Login(db.Model):
    """Login information which stores user information"""


    __tablename__ = "login"

    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Login: {}, Name: {}, Username: {}, password: {}, email: {}>".format(
                                                self.login_id, self.name, self.user_name,
                                               self.password, self.email)
                                               


class Advocate(db.Model):
    """Advocate information stored outside of login"""


    __tablename__ = "advocates"

    advocate_login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'), primary_key=True)
    position_name = db.Column(db.String(20), nullable=False)
    shelter_agency_id = db.Column(db.Integer, db.ForeignKey(
                                                'shelter_information.shelter_agency_id'))

    # Define relationship to Login
    login = db.relationship("Login", backref=db.backref("advocate", uselist=False))
                                             
    # Define relationship to Shelter_information
    shelter_information = db.relationship("Shelter_Information",
                           backref=db.backref("advocate"))
                                              
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Advocate Login Id: {}, Position Name: {}>".format(self.advocate_login_id,
                                               self.position_name)


class Victim(db.Model):
    """Victim information and relationship to which advocate"""


    __tablename__ = "victim"

    victim_login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'),
                                    primary_key=True)
    advocate_login_id = db.Column(db.Integer, db.ForeignKey('advocates.advocate_login_id'))

    # Define relationship to Login
    login = db.relationship("Login", backref=db.backref("victim", uselist=False))
                                              
    # Define relationship to Advocate
    advocate = db.relationship("Advocate", backref=db.backref("victim"))
                                             
  

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Victim login ID: {}, Advocate login ID: {}>".format(self.victim_login_id,
                                               self.advocate_login_id)

class Agency_Type(db.Model):
    """Specifications on types of agency forms will be submitted to"""


    __tablename__ = "agency_type"

    agency_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    agency_type = db.Column(db.String(100), nullable=False)
   
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Agency type ID: {}, agency type: {}>".format(self.agency_type_id,
                                               self.agency_type)


class Filled_Form(db.Model):
    """Information on which answers where answered on which form and by which victim."""

    __tablename__ = "filled_forms"

    filled_form_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.form_id'))
    victim_login_id = db.Column(db.Integer, db.ForeignKey('victim.victim_login_id'))
    time_filled = db.Column(db.TIMESTAMP, nullable=True)

    #Define relationship to Form
    form = db.relationship("Form", backref=db.backref('filled_forms'))

    #Define relationship to Victim
    victim = db.relationship("Victim", backref=db.backref('filled_forms'))
   
    def __repr__(self):
        """Provide helpful representation when printed."""

        return """<Filled Form ID: {}, Form ID: {}, Victim ID: {},
                 Time Filled: {}>""".format(self.filled_form_id, self.form_id,
                                            self.victim_login_id, self.time_filled)

class Form_Status(db.Model):
    """Information on which answers where answered on which form and by which victim."""

    __tablename__ = "form_status"

    filled_form_id = db.Column(db.Integer, db.ForeignKey('filled_forms.filled_form_id'), primary_key=True)
    app_received = db.Column(db.TIMESTAMP, nullable=False)
    app_pending = db.Column(db.TIMESTAMP, nullable=True)
    app_review = db.Column(db.TIMESTAMP, nullable=True)
    app_results = db.Column(db.String(1000), nullable=True)


    filled_form = db.relationship("Filled_Form", backref=db.backref("form_status", uselist=False))

class Direct_Message(db.Model):
    """Message text between client and advocate"""

    __tablename__ = "direct_message"

    direct_message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    victim_login_id = db.Column(db.Integer, db.ForeignKey('victim.victim_login_id'))
    advocate_login_id = db.Column(db.Integer, db.ForeignKey('advocates.advocate_login_id'))
    direct_message_text = db.Column(db.String(1000), nullable=False)
    sent_by = db.Column(db.String(100), nullable=False)

    victim = db.relationship("Victim",
                           backref=db.backref("direct_message"))

    advocate = db.relationship("Advocate",
                           backref=db.backref("direct_message"))





    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Direct Message Id: {}, Direct Message Text: {}>".format(self.direct_message_id,
                                               self.direct_message_text)




##############################################################################

def connect_to_db(app):
    """Connecting the database to our Flask Application"""
    
    #TODO name our postgres file
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///projectdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "You are connected to the database."
