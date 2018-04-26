import unittest

from server import app
import server

from model import db, Filled_Form
from test_seed import test_seed_data


def connect_to_db(app):
    """Connecting the database to our Flask Application"""
    
    #TODO name our postgres file
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

class Login(unittest.TestCase):

    def setUp(self):
        """Todo before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
    # Connect to test database
        connect_to_db(app)
        db.create_all()
        test_seed_data()

    def test_initial_page(self):
        """Testing initial login page"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('<title>  Login</title>', result.data)

    def test_login_advocate(self):
        """Test login for advocate"""
        result = self.client.post("/login",
                                  data={"username": "advocate_1",
                                        "password": "advocate1234"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You are logged in", result.data)

    def test_login_victim(self):
        """Test login for victim"""
        result = self.client.post("/login",
                                  data={"username": "victim_1",
                                        "password": "victim1234"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You are logged in", result.data)

    def test_login_wrong_username(self):
        """Test login for victim"""
        result = self.client.post("/login",
                                  data={"username": "asadlkjaslkdjakdj",
                                        "password": "victim1234"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Username does not exist", result.data)

    def test_login_wrong_password(self):
        """Test login for victim"""

        result = self.client.post("/login",
                                  data={"username": "advocate_1",
                                        "password": "djaskdajsajdlka"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Password incorrect, please try again.", result.data)

    def test_register_page(self):
        """Testing register page: client or advocate"""

        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1>Are you a Client or Advocate?</h1>", result.data)

    def test_register_route_client(self):
        """User entering client registration page"""
        result = self.client.post("/register",
                                  data={"advocate/client": "client"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("<br><label>Please choose an advocate<br>", result.data)

    def test_client_registration_post_route(self):
        """Client submitted registration infromation"""

        result = self.client.post("/register/client",
                                  data={"name": "Sara Smith",
                                        "email": "sara@gmail.com",
                                        "username": "sarah_v",
                                        "password": "client1234",
                                        "advocate": 1},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You are now registered! Please login.", result.data)

    def test_register_route_advocate(self):
        """User entering advocate registration page"""

        result = self.client.post("/register",
                                  data={"advocate/client": "advocate"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("<br><label>Please choose your shelter id number<br>", result.data)

    def test_advocate_registration_post_route(self):
        """Advocate submitted registration infromation"""

        result = self.client.post("/register/advocate",
                                  data={"username": "danielle_a",
                                        "password": "advocate1234",
                                        "name": "Danielle Smith",
                                        "email": "danielle@gmail.com",
                                        "position_title": "Invest Advocate",
                                        "shelter": 1},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You are now registered! Please login.", result.data)

    def tearDown(self):
        """Todo after each test."""

        db.session.close()
        db.drop_all()


class AdvocateLoggedIn(unittest.TestCase):
    def setUp(self):
        """Todo before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
    # Connect to test database
        connect_to_db(app)
        db.create_all()
        test_seed_data()

        with self.client as c:
            with c.session_transaction() as sess:
                #advocate
                sess["login_id"] = 2

        def mock_get_api_data_client(params):
            return [{u'City': u'MONTGOMERY', u'FirstName': u'DENNIS', u'LastName': u'RYAN', u'Comments': u'2014 BALDWIN COUNTY CONVICTION', u'DateOfBirth': u'7/30/1981', u'State': u'Mississippi', u'BondAmount': u'$0.00', u'CaseHistory': u'null', u'Type': u'Inmate', u'County': u'Baldwin', u'Eyes': u'Brown', u'Zip': u'48336', u'YearOfBooking': u'KILBY CORRECTIONS MONTGOMERY, AL , Montgomery County', u'Offence': u'[{"DESCRIPTION":"13A-6-66(a) - First Degree Sexual Abuse","DateConvicted":"01/08/2014","ConvictionState":"Alabama","ReleaseDate":"01/08/2014","Details":"FEMALE IN HER MID FORTIES"}]', u'BookingNo': u'BCSO12JBN002635', u'Address': u'KILBY CORRECTIONS MONTGOMERY, AL , Montgomery County', u'EntryDate': u'2017-04-13 02:28:42', u'BCType': u'POSSESSION OF CONTROLLED SUBSTANCE', u'CommonAddress': u'KILBY CORRECTIONS', u'Name': u'RYAN DENNIS', u'Gender': u'M', u'Age': u'27', u'CommonName': u'1877384', u'ReseasedDate': u'11/3/2012 10:08:00 AM', u'BirthYear': u'1981', u'STATE': u'MS', u'Race': u'Black', u'Sariff': u"Baldwin County Sheriff's Office", u'BookingDate': u'11/03/2012 01:39:56', u'MNINo': u'BCSO12MNI003788', u'AddressGiven': u'KILBY CORRECTIONS MONTGOMERY, AL , Montgomery County', u'Weight': u'210lbs', u'PHOTO': u'http://pixialiate.backgroundcheckapi.com/photo@alabama@baldwin@1877384-23981476.jpg', u'Height': u"6'00''", u'Hair': u'Black', u'Registration': u'3398', u'CurrentStatus': u'Released', u'Aliases': u'MOOKIE'}]

        server.get_api_data = mock_get_api_data_client


    def test_logout(self):
        """Test logout process"""
        result = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Logged Out.", result.data)

    def test_welcome(self):
        """Test welcome page for Advocate"""
        #TODO how to test to make sure only advocate are viewing the View Clients Page
        result = self.client.get("/welcome")
        self.assertEqual(result.status_code, 200)
        self.assertIn("View Clients", result.data)

    def test_advocate_page(self):
        """Test to see if advocate is able to see all their clients and their
        clients filled forms"""

        result = self.client.get("/advocate")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1>Clients' Filled Out Forms</h1>", result.data)

    def test_client_filled_form_safety_plan(self):
        """Test to see if advocate when click on safety plan will enter a page
        where they can see victim's answers to the questions on the filled form"""
        #QUESTION: to see if advocate is viewing the correct form

        result = self.client.get("/advocate/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Im ok', result.data)

    def test_client_filled_form_victim_compensation(self):
        """Test to see if advocate when click on victim compensation form will enter a page
        where they can see victim's answers to the questions on the filled form"""
        #QUESTION: to see if advocate is viewing the correct form

        result = self.client.get("/advocate/2")
        self.assertEqual(result.status_code, 200)
        self.assertIn("04/24/2018", result.data)

    def test_advocate_view_shelter(self):
        """Test that advocate can properly see the shelter page"""

        result = self.client.get("/shelter")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Time the next bed will be available:", result.data)

    def test_advocate_edit_shelter(self):
        """Test advocate is able to edit the status of the shelter"""
        result = self.client.post("/shelter",
                                  data={"number_available_beds": 4,
                                        "time_available_beds": 'Monday, February 01, 2018'},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1> Welcome </h1>", result.data)

    def test_advocate_view_legal(self):
        """Test that advocate can properly see the legal advocacy page"""

        result = self.client.get("/legal")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1>Legal Advocacy</h1>", result.data)


    def test_legal_post_client(self):
        """Test if advocate can accurately search for defendant on legal page"""

        result = self.client.get("/legal-background",
                                  data={"fname": "",
                                        "lname": "Ryan",
                                        "mname": "",
                                        "state": "",
                                        "county": "",
                                        "city": "",
                                        "birthyear": ""})                                     
        self.assertEqual(result.status_code, 200)
        self.assertIn("<b>First Name:</b> DENNIS<br>", result.data)


    def tearDown(self):
        """Todo after each test."""

        db.session.close()
        db.drop_all()

class VictimLoggedIn(unittest.TestCase):
    def setUp(self):
        """Todo before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
    # Connect to test database
        connect_to_db(app)
        db.create_all()
        test_seed_data()

        with self.client as c:
            with c.session_transaction() as sess:
                #advocate
                sess["login_id"] = 1

        def mock_get_api_data_client(params):
            return [{u'FirstName': u'CHANTELL MORNEAK', u'LastName': u'SMITH', u'DateOfBirth': u'5/28/1976', u'State': u'Georgia', u'BondAmount': u'$0.00', u'Type': u'Inmate', u'YearOfBooking': u'2012', u'EntryDate': u'2017-03-23 22:36:50', u'BCType': u'Released Inmate', u'Name': u'SMITH, CHANTELL MORNEAK', u'Gender': u'FEMALE', u'Age': u'36', u'CommonName': u'SMITH, CHANTELL MORNEAK', u'ReseasedDate': u'6/18/2012 6:00:00 AM', u'BirthYear': u'1976', u'STATE': u'GA', u'Race': u'B', u'Sariff': u'Douglas Count Sheriff\'s Office', u'BookingDate': u'06/15/2012 08:31:09', u'MNINo': u'DCSO01MNI044420', u'BookingNo': u'DCSO12JBN005043', u'CaseHistory': u'null', u'County': u'Douglas', u'PHOTO': u'http://pixialiate.backgroundcheckapi.com/photo@georgia@douglas@85227-GA-DOUGLAS-DCSO12JBN005043.jpg', u'CurrentStatus': u'Released'}]

        server.get_api_data = mock_get_api_data_client


    def test_welcome(self):
        """Test welcome page for victim"""
        #TODO how to test to make sure only advocate are viewing the View Clients Page
        result = self.client.get("/welcome")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1> Welcome </h1>", result.data)

    def test_financial_get(self):
        """Test Victim Compensation Page"""

        result = self.client.get("/financial")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h2>Victim Compensation Application</h2>", result.data)

    def test_financial_post(self):
        """Test Victim Compensation Page"""

        result = self.client.post("/financial",
                                  data={"form_id": 2,
                                    "section_1_1": "Christine Smith",
                                    "section_1_2": "",
                                    "section_1_3": "",
                                    "section_1_4": "",
                                    "section_1_5": "",
                                    "section_1_6": "",
                                    "section_1_7": "",
                                    "section_1_8": "",
                                    "section_1_9": "",
                                    "section_1_10": "",
                                    "section_1_11": "",
                                    "section_1_12": "",
                                    "section_1_13": "",
                                    "section_2_14": "",
                                    "section_2_15": "",
                                    "section_2_16": "",
                                    "section_2_17": "",
                                    "section_2_18": "",
                                    "section_3_19": "",
                                    "section_3_20": "",
                                    "section_3_21": "",
                                    "section_3_22": "",
                                    "section_3_23": "",
                                    "section_3_24": "",
                                    "section_3_25": "",
                                    "section_3_26": "",
                                    "section_3_27": "",
                                    "section_4_28": "",
                                    "section_4_29": "",
                                    "section_4_30": "",
                                    "section_4_31": "",
                                    "section_4_32": "",
                                    "section_4_33": "",
                                    "section_4_34": "",
                                    "section_4_35": "",
                                    "section_4_36": "",
                                    "section_4_37": "",
                                    "section_4_38": "",
                                    "section_4_39": "",
                                    "section_4_40": "",
                                    "section_5_41": "",
                                    "section_5_42": "",
                                    "section_5_43": "04/25/2018"},
                                        # "filled_form": 3}
                                    follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn("You have successfully submitted your Victim Compensation Application", result.data)
        filled_form_3 = db.session.query(Filled_Form).filter_by(filled_form_id=3).first()
        # print filled_form_3
        #list of object answers
        answers = filled_form_3.answers
        answer_1 = answers[0]
        self.assertIn("Christine Smith", answer_1.answer_text)

    def test_safety_plan_get(self):
        """Test Safety Plan Page"""

        result = self.client.get("/safety-plan")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1> Safety Plan</h1>", result.data)

    def test_safety_plan_post(self):
        """Test Victim Compensation Page"""

        result = self.client.post("/safety-plan",
                                  data={"form_id": 1,
                                        "section_1_1": "yes",
                                        "section_1_2": "no",
                                        "section_1_3": "no",
                                        "section_2_4": "no",
                                        "section_2_5": "decline",
                                        "section_2_6": "decline",
                                        "section_2_7": "decline",
                                        "section_2_8": "decline",
                                        "section_2_9": "decline",
                                        "section_2_10": "decline",
                                        "section_2_11": "no",
                                        "section_3_12": "y"},
                                    follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn("You have successfully submitted your Safety Plan Form", result.data)
        filled_form_3 = db.session.query(Filled_Form).filter_by(filled_form_id=3).first()
        # print filled_form_3
        # #list of object answers
        answers = filled_form_3.answers
        answer_1 = answers[0]
        self.assertIn("yes", answer_1.answer_text)

    def test_client_view_shelter(self):
        """Test that client can properly see the shelter page"""

        result = self.client.get("/shelter")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<b>Available beds:</b>", result.data)

    def test_client_view_legal(self):
        """Test that client can properly see the legal advocacy page"""

        result = self.client.get("/legal")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h1>Legal Advocacy</h1>", result.data)

    def test_legal_post_advocate(self):
        """Test if client an accurately search for defendant"""

        result=self.client.get("/legal-background",
                                  data={"fname": "",
                                        "lname": "Smith",
                                        "mname": "",
                                        "state": "",
                                        "county": "",
                                        "city": "",
                                        "birthyear": ""})
        self.assertEqual(result.status_code, 200)
        self.assertIn("<b>First Name:</b> CHANTELL MORNEAK<br>", result.data)

    def tearDown(self):
        """Todo after each test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
