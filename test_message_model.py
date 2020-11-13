"""Tests for the message SQLAlchemy model"""


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

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

# db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data"""
        self.client = app.test_client()

        db.drop_all()
        db.create_all()

        # Create some users, to use for the messages' user ids
        user1 = User.signup('testuser1', 'email1@gmail.com', 'password1', None, None)
        user1_id = 100
        user1.id = user1_id

        user2 = User.signup('testuser2', 'email2@gmail.com', 'password2', None, None)
        user2_id = 200
        user2.id = user2_id

        user3 = User.signup('testuser3', 'email3@gmail.com', 'password3', None, None)
        user3_id = 300
        user3.id = user3_id

        db.session.commit()

        u1 = User.query.get(user1_id)
        u2 = User.query.get(user2_id)
        u3 = User.query.get(user3_id)


        self.u1 = u1
        self.uid1 = user1_id

        self.u2 = u2
        self.uid2 = user2_id

        self.u3 = u3
        self.uid3 = user3_id

        m1 = Message(text='message1_text', user_id=100)
        m1.id = 100
        
        m2 = Message(text='message2_text', user_id=200)
        m2.id = 200

        db.session.add(m1)
        db.session.add(m2)

        db.session.commit()

        self.m1 = m1
        self.m2 = m2

    def tearDown(self):
        db.session.rollback()

    def test_message_model(self):
        """Most basic test to check if model works"""
        m = Message(text='message_text', user_id=self.uid3)

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u3.messages), 1)
        self.assertEqual(self.u3.messages[0].text, 'message_text')
        self.assertEqual(len(self.u1.messages), 1)
        self.assertEqual(self.u1.messages[0].text, 'message1_text')

    
    def test_message_ownership(self):
        """Does the database correctly identify the user who created a message?"""
        self.assertEqual(self.m1.user, self.u1)
        self.assertEqual(self.m2.user, self.u2)
        self.assertNotEqual(self.m1.user, self.u2)
        self.assertNotEqual(self.m2.user, self.u1)

    def test_message_likes(self):
        """Do likes on a message properly work?"""

        self.u1.likes.append(self.m1)
        self.u2.likes.append(self.m2)

        db.session.commit()

        likes = Likes.query.all()
        self.assertEqual(len(likes), 2)
        self.assertEqual(likes[0].message_id, self.m1.id)
        self.assertEqual(likes[0].user_id, self.u1.id)
        self.assertEqual(likes[1].message_id, self.m2.id)
        self.assertEqual(likes[1].user_id, self.u2.id)
