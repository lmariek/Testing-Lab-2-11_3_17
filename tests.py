import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        # app.config['SECRET_KEY'] = 'key'
        # self.client = app.test_client()

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #       sess['user_id'] = 1

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        result = self.client.get("/")
        self.assertNotIn("Party Details", result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertIn("Party Details", result.data)
        self.assertNotIn("Please RSVP", result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
              sess['RSVP'] = True

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):

        result = self.client.get("/games")
        self.assertIn("Monopoly", result.data)


if __name__ == "__main__":
    unittest.main()
