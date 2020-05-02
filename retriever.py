"""
Recipe Retriever for Arbitrary Search Source
"""

from bs4 import BeautifulSoup
import requests


class Retriever:
    USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                'Chrome/81.0.4044.113 Safari/537.36'
    HTTP_HEADERS = {'User-Agent': USERAGENT}

    def __init__(self, ingredients):
        """
        :param ingredients: (List[str]) list of ingredients from client
        """

        self.handlers = {
            'allrecipes': self.allrecipes,
            'foodnetwork': self.foodnetwork,
            'epicurious': self.epicurious
        }

        self.ingredients = ingredients

    def allrecipes(self):
        """
        Parsing recipes and ingredients from allrecipes.com using their ingredient search.
        Sorting by allrecipes default sorter when using ingredient search
        """

        url = f"https://allrecipes.com/search/results/?ingIncl={','.join(self.ingredients)}&sort=re"
        html = requests.get(url, headers=Retriever.HTTP_HEADERS)

        soup = BeautifulSoup(html.text, "html.parser")

        return [product['href'] for product in soup.find_all("a", "fixed-recipe-card__title-link", href=True)]

    def foodnetwork(self):
        """
        Parsing recipes and ingredients from foodnetwork.com, they dont have specific ingredient search
        food network already sorts their own recipes by their famous chefs
        """

        url = f"https://www.foodnetwork.com/search/{'-'.join(self.ingredients)}-"
        html = requests.get(url, headers=Retriever.HTTP_HEADERS)

        soup = BeautifulSoup(html.text, "html.parser")

        return ['https:' + product['href'] for product in soup.find_all("a", "m-Rating__a-StarsLink", href=True)]

    def epicurious(self):
        """
        Parsing recipes and ingredients from epicurious.com, they have an ingredient search, but not great
        Sorting by most rated and only pulling recipes that are above 80% make it again
        """

        url = f"https://www.epicurious.com/search/?sort=mostReviewed&include={'%2C'.join(self.ingredients)}"
        html = requests.get(url, headers=Retriever.HTTP_HEADERS)

        soup = BeautifulSoup(html.text, "html.parser")

        return [('https://www.epicurious.com' + product['href']) for product in
                soup.find_all("a", "show-quick-view", href=True)]

    def __call__(self, handlers):
        """
        This calls the associated handlers with those passed in and returns the results in a dictionary
        :param handlers :list of string handlers to return results from
        """
        recipes = {}
        for handler in handlers:
            recipes[handler] = self.handlers[handler]()

        return recipes
