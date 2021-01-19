
from unittest import TestCase
from app import app
from models import db, User, Favorites
from flask import session

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///mixology"
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

user_data ={
    "username":"bigbob22", 
    "password": "greenteam2", 
    "first_name": "bob"
}

class UserViewsTestCase(TestCase):
    """Tests for views about users."""

    def setUp(self):
        """Make demo data."""

        User.query.delete()

        user = User(user_data)
        db.session.add(user)
        db.session.commit()

        self.user= user

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_registration(self):
        """Test client registration."""
        with app.test_client() as client:
            resp= client.get("/register")
            self.assertEqual(resp.status_code, 200)

            new_user= client.post('/register', data={"username": "hellothere", 'password': "woopwoop22", "first_name": "Bob"},
                         follow_redirects=True)
            self.assertEqual(new_user.status_code, 302)
            self.assertEqual(new_user.location, "http://localhost/main")
            self.assertEqual(session['username'], "hellothere")

    def test_login(self):
        """Test login."""
        with app.test_client() as client:
            resp = client.get("/login")
            self.assertEqual(resp.status_code, 200)

            login= client.post('/login', data={"username": "bigbob22", 'password': "greenteam2"},
                         follow_redirects=True)
            self.assertEqual(login.status_code, 302)
            self.assertEqual(login.location, "http://localhost/main")
            self.assertEqual(session['username'], "bigbob22")

    def test_logout(self):
        with app.test_client() as client:
            resp = client.get("/logout", follow_redirects=True)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")
            self.assertFalse(session['username'])

    def test_form_search_direction(self):
        with app.test_client() as client:
            resp = client.post('/ingredient-search', data={"search_term": "Gin"})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual("search_term", "Gin")
            
    def test_thumbnail_search_direction(self):
        with app.test_client() as client:
            resp = client.get('/vodka-search-results')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual("search_term", "Vodka")