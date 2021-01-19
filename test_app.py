from unittest import TestCase
from app import app
from flask import session

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class AppViewsTestCase(TestCase):

    def age_verify_form(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Age Verification</h3>', html)

    def test_registration_submit(self):
        with app.test_client() as client:
            resp = client.post('/register',
                               data={'username': 'blue', 'password': 'blue123', 'first_name': 'bob'})

            self.assertEqual(resp.status_code, 302)
            self.assertIn(session['username'], 'blue')

    def test_redirection(self):
        with app.test_client() as client:
            resp = client.get("/logout")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/main")

    def test_input_search(self):
        with app.test_client() as client:
            resp = client.get("/vodka-search", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="resultsTitle">Vodka</h2>', html)
