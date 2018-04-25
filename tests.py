import unittest

from server import app

from model import db
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

    def test_client_filled_form_question_answer(self):
        """Test to see if advocate when click on filled form will enter a page
        where they can see victim's answers to the questions on the filled form"""
        #QUESTION: to see if advocate is viewing the correct form

        result = self.client.get("/advocate/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn('Im ok', result.data)

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


    def test_welcome(self):
        """Test welcome page for Advocate"""
        #TODO how to test to make sure only advocate are viewing the View Clients Page
        result = self.client.get("/welcome")
        self.assertEqual(result.status_code, 200)
        self.assertIn("<h2>Safety Plan</h2>", result.data)

    def tearDown(self):
        """Todo after each test."""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
