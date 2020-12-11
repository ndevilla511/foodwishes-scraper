import requests
from bs4 import BeautifulSoup


def scrape_allrecipes(url):
    """
    Scrapes an allrecipes recipe page and returns a recipe dictionary
    :param url: enter the URL for an allrecipes page
    """

    allrecipes_page = requests.get(url)
    soup = BeautifulSoup(allrecipes_page.content, features="html.parser")
    recipe_dict = {}

    recipe_title = soup.find("h1", "headline heading-content").text.strip()

    recipe_dict["recipe_title"] = recipe_title

    ingrd_fieldsets = soup.find_all("fieldset", "ingredients-section__fieldset")

    recipe_dict["ingredients"] = []
    for fieldset in ingrd_fieldsets:

        legend = fieldset.find("legend", class_="section-subheadline")
        if legend:
            legend = legend.text.strip()
        ingrds_list = []

        ingrds = fieldset.find_all("span", class_="ingredients-item-name")
        for ingrd in ingrds:
            ingrds_list.append(ingrd.text.strip())

        recipe_dict["ingredients"].append({legend: ingrds_list})

    instructions_section_items = soup.find_all("li", class_="instructions-section-item")

    recipe_dict["instructions"] = []
    for item in instructions_section_items:
        recipe_dict["instructions"].append(item.find("p").text.strip())

    notes_section = soup.find("div", class_="recipe-note")

    recipe_dict["chefs_notes"] = []
    if notes_section:
        for note in notes_section.find_all("p"):
            recipe_dict["chefs_notes"].append(note.text.strip())

    return recipe_dict