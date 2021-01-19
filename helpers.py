import requests
from models import Recipe


def search_by_ingredient(ingredient):
    response = requests.get(
        f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}")
    r = response.json()
    drinks = r["drinks"]
    return drinks


def search_by_name(drink_name):
    response = requests.get(
        f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name}")
    r = response.json()
    drinks = r["drinks"]
    return drinks


def search_by_letter(first_letter):
    response = requests.get(
        f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={first_letter}")
    r = response.json()
    drinks = r["drinks"]
    return drinks


def search_by_id(drink_id):
    response = requests.get(
        f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={drink_id}")
    r = response.json()
    drinks = r["drinks"]
    return drinks


def search_by_non_alcoholic():
    response = requests.get(
        "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic")
    r = response.json()
    drinks = r["drinks"]
    return drinks


def get_random_selection():
    response = requests.get(
        "https://www.thecocktaildb.com/api/json/v1/1/random.php")
    r = response.json()
    drinks = r["drinks"]

    return drinks


def get_all_ingredients_list():
    response = requests.get(
        "https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list")
    r = response.json()
    drinks = r["drinks"]
    ingredients = [drink["strIngredient1"] for drink in drinks]

    ingredients.sort()
    return ingredients


def create_recipe_obj(drink_id):
    drinks = search_by_id(drink_id)
    ingredients = []
    measurements = []
    for drink in drinks[0]:
        if drink.startswith('strIngredient'):
            if drinks[0][drink]:
                ingredients.append(drinks[0][drink])
    for drink in drinks[0]:
        if drink.startswith('strMeasure'):
            if drinks[0][drink]:
                measurements.append(drinks[0][drink])
    ingredients_dict = [(measurements[i], ingredients[i])
                        for i in range(0, len(measurements))]
    img = drinks[0]["strDrinkThumb"]
    name = drinks[0]["strDrink"]
    glass = drinks[0]["strGlass"]
    drink_id = drinks[0]["idDrink"]
    instructions = drinks[0]["strInstructions"]
    recipe = Recipe(name=name, instructions=instructions,
                    ingredients=ingredients_dict, img=img, glass=glass, drink_id=drink_id)
    return recipe
