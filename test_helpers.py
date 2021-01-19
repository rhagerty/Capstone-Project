import json
from unittest import TestCase
from helpers import search_by_ingredient, get_all_ingredients_list, create_recipe_obj

class HelpersTestCase(TestCase):
    def test_ingredient_search(self):
        self.assertIsInstance(search_by_ingredient('vodka'), list)
        self.assertIn('Vodka', search_by_ingredient('vodka'))

    def test_all_ingredients_list(self):
        self.assertNotIn('strIngredient', get_all_ingredients_list())

    def test_recipe_obj(self):
        self.assertIsInstance(create_recipe_obj('11121'), dict)
        self.assertIn('Scotch', create_recipe_obj('11121'))
        self.assertNotIn('strIngredient', create_recipe_obj('11121'))