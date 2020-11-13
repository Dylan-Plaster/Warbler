"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        # User.query.delete()
        # Message.query.delete()
        # Follows.query.delete()

        self.client = app.test_client()

        db.drop_all()
        db.create_all()

        user1 = User.signup('testuser1', 'email1@gmail.com', 'password1', None, None)
        user1_id = 100
        user1.id = user1_id

        user2 = User.signup('testuser2', 'email2@gmail.com', 'password2', None, None)
        user2_id = 200
        user2.id = user2_id

        db.session.commit()

        u1 = User.query.get(user1_id)
        u2 = User.query.get(user2_id)

        self.u1 = u1
        self.uid1 = user1_id

        self.u2 = u2
        self.uid2 = user2_id
        

    def tearDown(self):
        """Rollback"""
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_user_repr(self):
        """Does the repr method display the user's correct info?"""

        self.assertEqual(self.u1.__repr__(), "<User #100: testuser1, email1@gmail.com>")
        self.assertEqual(self.u2.__repr__(), "<User #200: testuser2, email2@gmail.com>")

    def test_is_follows(self):
        """Does is_following correctly detect when a user follows another user?"""
        
        # user 1 follows user 2:
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertEqual(self.u1.following[0], self.u2)
        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))
    
    def test_is_followed_by(self):
        """Test the is_followed_by method"""
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))

    def test_user_signup(self):
        """Test the user signup method"""
        username = "testuser3"
        email = "email3@gmail.com"
        password = "password3"
        image_url = None
        header_image_url = None

        
        u3 = User.signup(username, email, password, image_url, header_image_url)
        u3.id = 999

        db.session.commit()

        user_test = User.query.get(999)

        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.username, 'testuser3')
        self.assertEqual(user_test.email, 'email3@gmail.com')

        # Make sure the password is not being stored in plaintext format!:
        self.assertNotEqual(user_test.password, 'password3')

        # Now check to make sure User.signup() fails when given invalid input:
        invalid = User.signup(username=None, email="email4@gmail.com", password="password4", image_url=image_url, header_image_url=header_image_url)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_user_authenticate(self):
        """Test User.authenticate method"""
        
        self.assertIsInstance(User.authenticate(username='testuser2', password='password2'), User)
        self.assertTrue(User.authenticate(username='testuser1', password='password1'))
        self.assertFalse(User.authenticate(username='testuser1', password='password2'))
        self.assertFalse(User.authenticate(username='testuser2340293', password='password1'))
        

