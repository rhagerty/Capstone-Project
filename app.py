from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Favorites
from forms import UserForm, UserLoginForm
from sqlalchemy.exc import IntegrityError
from itertools import chain
import json
from helpers import search_by_non_alcoholic, search_by_ingredient, search_by_id, get_random_selection, search_by_name, search_by_letter, create_recipe_obj, get_all_ingredients_list
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("postgres://amherlzrmpbgkj:9778f982542fd9d280d3bf6c2ca72ca3f8ad0e500d5ea7fe7e01539b04a53909@ec2-34-192-72-159.compute-1.amazonaws.com:5432/dc4g08tsniskto", 'postgres///mixology')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "nevertell"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route("/")
def age_check():
    """Show age verification popup."""

    return render_template("ageverify.html")


@app.route("/main")
def homepage():
    """Show homepage."""

    return render_template("main.html")


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Show form to register new user"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        new_user = User.register(username, password, first_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username

        return redirect('/main')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Show user login form"""
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect('/main')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    """Log out current user"""
    session.pop('username')

    return redirect('/main')


@app.route('/<input>-search', methods=['GET', 'POST'])
def display_form_search_results(input):
    """Show search bar search results list"""
    search_term = (request.form[f'{input}']).capitalize()

    if input == "ingredient":
        drinks = search_by_ingredient(search_term)
    elif input == "name":
        drinks = search_by_name(search_term)
    elif input == "letter":
        drinks = search_by_letter(search_term)

    return render_template("/results.html", drinks=drinks, search_term=search_term)


@app.route('/<search_term>-search-results', methods=['GET', 'POST'])
def display_thumbnail_search_results(search_term):
    """Main page thumbnail search results"""

    search_term = search_term.capitalize()
    if search_term == "Non-alcoholic":
        drinks = search_by_non_alcoholic()
    else:
        drinks = search_by_ingredient(search_term)

    return render_template("/results.html", drinks=drinks, search_term=search_term)


@app.route('/get-random-selection', methods=['GET', 'POST'])
def display_random():
    """Generate a random selection"""
    drinks = get_random_selection()
    drink_id = drinks[0]["idDrink"]

    return redirect(f"/display-recipe/{drink_id}")


@app.route('/all-ingredients-list', methods=['GET', 'POST'])
def display_all_ingredients():
    ingredients = get_all_ingredients_list()
    return render_template("all_ingredients.html", ingredients=ingredients)


@app.route('/display-recipe/<drink_id>', methods=['GET', 'POST'])
def display_recipe(drink_id):
    """Display recipe details"""
    recipe = create_recipe_obj(drink_id)

    return render_template("displayrecipe.html", recipe=recipe)


@app.route('/save-to-favorites/<drink_id>', methods=['GET', 'POST'])
def save_to_favorites(drink_id):
    """Save recipe to favorites"""
    if session['username']:
        new_favorite = Favorites(
            username=session['username'], drink_id=drink_id)
        db.session.add(new_favorite)
        db.session.commit()
        session['favorites'] = {new_favorite.drink_id: new_favorite.id}
        flash("Recipe saved! Click My Mixology to see all saved recipes.")
        return redirect(f"/display-recipe/{drink_id}")
    else:
        flash("You must be logged in to save recipes!")
        return redirect(f"/display-recipe/{drink_id}")


@app.route('/<username>/favorites', methods=['GET', 'POST'])
def display_favorites(username):
    """display a user's favorites on page"""
    u = User.query.filter_by(username=username).first()
    first_name = u.first_name.capitalize()
    favorites = Favorites.query.filter_by(username=username).all()
    drink_ids = []
    drinks = []
    for favorite in favorites:
        drink_ids.append(favorite.drink_id)
    for drink_id in drink_ids:
        drinks.append(search_by_id(drink_id))

    drinks = (list(chain.from_iterable(drinks)))
    return render_template("/favorites.html", drinks=drinks, first_name=first_name)


@app.route('/remove-from-favorites/<drink_id>', methods=['GET', 'POST'])
def remove_from_favorites(drink_id):
    """remove a user's favorite"""
    session['favorites'].pop(f"{drink_id}")
    Favorites.query.filter_by(drink_id=drink_id).delete()
    db.session.commit()
    flash("Recipe removed from favorites!")
    return redirect(f"/display-recipe/{drink_id}")
