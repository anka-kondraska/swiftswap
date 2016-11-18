from unittest import TestCase

import sys
sys.path.append('..')
from barter_network import app

from model import connect_to_db, db, User, Skill, UserSkill, sample_data


class FlaskTests(TestCase):
    """Flask testing basic page info"""

    def setUp(self):
        """To do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test homepage"""

        result = self.client.get("/")
        self.assertIn("Welcome to Barter Network", result.data)

class FlaskTestsDatabase(TestCase):
    """Flask testing that use database"""

    def setUp(self):
        """Before every test"""
        self.client = app.test_client()
        app.config["TESTING"] = True

        connect_to_db(app, "postgresql:///barternet")

        db.create_all()
        sample_data()

    def test(self):
        pass




    def tearDown(self):
        pass




if __name__ == "__main__":
    import unittest

    unittest.main()