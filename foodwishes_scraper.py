import requests
import re
import json
from bs4 import BeautifulSoup
from allrecipes_scraper import scrape_allrecipes


def get_foodwishes_recipes(number=10):
    """
    uses the allrecipes_scraper function, returns json with a list of recipe objects from the latest number of posts
    from Chef John's blog, foodwishes.com
    :param number: pulls up last number of posts from Chef John's blog, limit up to 49
    """
    foodwishes_page = requests.get(f"https://foodwishes.blogspot.com/search?max-results={number}")
    soup = BeautifulSoup(foodwishes_page.content, features="html.parser")
    recipe_links = []
    recipes = {}

    for link in soup.findAll('a', attrs={'href': re.compile("^https://www.allrecipes.com/recipe/")}):
        recipe_links.append(link.get('href'))
    recipe_links = list(dict.fromkeys(recipe_links))

    recipe_list = [scrape_allrecipes(link) for link in recipe_links]
    recipes["recipe_list"] = recipe_list
    with open("foodwishes_recipes.json", "a") as foodwishes:
        json.dump(recipes, foodwishes)

if __name__ == "__main__":
    print(get_foodwishes_recipes(10))