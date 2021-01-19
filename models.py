from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), nullable=False,
                         primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, pwd, first_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, first_name=first_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False


class Recipe:
    def __init__(self, name, ingredients, img, glass, drink_id, instructions):
        self.name = name
        self.ingredients = ingredients
        self.img = img
        self.glass = glass
        self.drink_id = drink_id
        self.instructions = instructions


class Favorites(db.Model):

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    username = db.Column(db.Text, db.ForeignKey('users.username'))
    drink_id = db.Column(db.Integer, nullable=False)
