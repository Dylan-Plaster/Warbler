import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, connect_db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, do_login
from flask import session

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ViewTestCase(TestCase):
    """Test view routes"""

    def setUp(self):
        """Create test client, add sample data"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.u1 = User.signup(username='testuser1',email='email1@gmail.com', password='password1', image_url=None, header_image_url=None)
        self.u1_id = 100
        self.u1.id = self.u1_id

        self.u2 = User.signup(username='testuser2',email='email2@gmail.com', password='password2', image_url=None, header_image_url=None)
        self.u2_id = 200
        self.u2.id = self.u2_id

        self.u3 = User.signup(username='testuser3',email='email3@gmail.com', password='password3', image_url=None, header_image_url=None)
        self.u3_id = 300
        self.u3.id = self.u3_id

        db.session.commit()


    def tearDown(self):
        db.session.rollback()
    

    def test_signup(self):
        
        with self.client as client:
            # Test GET /signup, make sure it shows the signup form
            resp = client.get('/signup')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Join Warbler today.', html)

            # Test POST /signup. Make sure it redirects to / on valid signup
            resp = client.post('/signup', data={'username':'testuser4', 'password':'password4', 'email':'email4@gmail.com'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/')
            
    def test_login(self):
        with self.client as client:
            # Test GET /login make sure it shows the form
            resp = client.get('/login')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="join-message">Welcome back.</h2>', html)
            self.assertIn('<form method="POST" id="user_form">', html)


            # Test POST /login with valid data
            data = {'username':'testuser1' , 'password': 'password1'}
            resp = client.post('/login', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hello, testuser1!', html)

    def test_users_index(self):
        with self.client as client:
            resp = client.get('/users')

            self.assertIn('testuser1', str(resp.data))
            self.assertIn('testuser2', str(resp.data))
            self.assertIn('testuser3', str(resp.data))

    def test_users_search(self):
        with self.client as client:
            resp = client.get('/users?q=testuser1')

            self.assertIn('testuser1', str(resp.data))
            
            self.assertNotIn('testuser2', str(resp.data))
            self.assertNotIn('testuser3', str(resp.data))

    def test_users_show(self):
        with self.client as client:
            resp = client.get('/users/100')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.u1.username, html)
    
    def test_show_following(self):
        with self.client as client:
            # No user is logged in; this should redirect to '/' 
            resp = client.get('/users/100/following')

            self.assertEqual(resp.status_code, 302)

            # Ok, now let's log in and check that show_following works:
            data = {'username' : 'testuser1', 'password' : 'password1'}
            resp = client.post('/login', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            # Quickly check to make sure login succeeded before testing show_following:
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hello, testuser1!', html)
            self.assertEqual(session['curr_user'], 100)

            # Add some follows between out test users:
            f1 = Follows(user_being_followed_id=self.u2_id, user_following_id=self.u1_id)
            f2 = Follows(user_being_followed_id=self.u3_id, user_following_id=self.u1_id)
            

            db.session.add_all([f1,f2])
            db.session.commit()

            resp = client.get('/users/100/following')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser2', html)








            
    


