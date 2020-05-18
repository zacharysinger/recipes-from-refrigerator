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

        recipe_urls = []
        # img_urls = []
        recipe_names = []

        link_counter = 0
        name_counter = 0
        limit = 10

        url = f"https://allrecipes.com/search/results/?ingIncl={','.join(self.ingredients)}&sort=re"
        html = requests.get(url, headers=Retriever.HTTP_HEADERS)
        soup = BeautifulSoup(html.text, "html.parser")

        for a in soup.find_all("a", "fixed-recipe-card__title-link", href=True):
            recipe_urls.append(a["href"])
            link_counter += 1
            if link_counter == limit:
                break

        # for b in soup.find_all("img", "fixed-recipe-card__img"):
        #     img_urls.append(b.get("data-original-src"))
        #     counter += 1
        #     if counter == limit:
        #         break

        for c in soup.find_all("span", "fixed-recipe-card__title-link"):
            recipe_names.append(c.text.strip())
            name_counter += 1
            if name_counter == limit:
                break

        return recipe_urls, recipe_names

    def foodnetwork(self):
        """
        Parsing recipes and ingredients from foodnetwork.com, they dont have specific ingredient search
        food network already sorts their own recipes by their famous chefs
        """

        recipe_urls = []
        # img_urls = []
        recipe_names = []

        link_counter = 0
        name_counter = 0
        limit = 10

        url = f"https://www.foodnetwork.com/search/{'-'.join(self.ingredients)}-"
        html = requests.get(url, headers=Retriever.HTTP_HEADERS)
        soup = BeautifulSoup(html.text, "html.parser")

        for a in soup.find_all("a", "m-Rating__a-StarsLink", href=True):
            recipe_urls.append('https:' + a['href'])
            link_counter += 1
            if link_counter == limit:
                break

        # for b in soup.find_all("img", "m-MediaBlock__a-Image"):
        #     img_urls.append(b.get("src"))
        #     counter += 1
        #     if counter == limit:
        #         break

        for c in soup.find_all("span", "m-MediaBlock__a-HeadlineText"):
            recipe_names.append(c.text.strip())
            name_counter += 1
            if name_counter == limit:
                break

        return recipe_urls, recipe_names

    def epicurious(self):
        """
        Parsing recipes and ingredients from epicurious.com, they have an ingredient search, but not great
        Sorting by most rated and only pulling recipes that are above 80% make it again
        """

        recipe_urls = []
        # img_urls = []
        recipe_names = []

        link_counter = 0
        name_counter = 0
        limit = 10

        url = f"https://www.epicurious.com/search/?sort=mostReviewed&include={'%2C'.join(self.ingredients)}"
        html = requests.get(url, headers=Retriever.HTTP_HEADERS)
        soup = BeautifulSoup(html.text, "html.parser")

        for a in soup.find_all("a", "show-quick-view", href=True):
            recipe_urls.append('https://www.epicurious.com' + a['href'])
            link_counter += 1
            if link_counter == limit:
                break

        # epicurious photos do not work since they are added to the site with JS after load

        # for b in soup.find_all("a", "photo-link", href=True):
        #     photo_url = 'https://www.epicurious.com' + b['href']
        #     new_html = requests.get(photo_url, headers=Retriever.HTTP_HEADERS)
        #     new_soup = BeautifulSoup(new_html.text, "html.parser")
        #     for z in new_soup.find_all("img", "photoloaded"):
        #         img_urls.append(z.get("srcset"))

        for c in soup.find_all("h4", "hed"):
            for z in c.find_all("a"):
                recipe_names.append(z.text.strip())
                name_counter += 1
                if name_counter == limit:
                    break

        return recipe_urls, recipe_names

    def __call__(self, handlers):
        """
        This calls the associated handlers with those passed in and returns the results in a dictionary
        :param handlers :list of string handlers to return results from
        """
        recipe_urls = {}
        # img_urls = {}
        recipe_names = {}
        for handler in handlers:
            recipe_urls[handler] = self.handlers[handler]()
            # img_urls[handler] = self.handlers[handler]()
            recipe_names[handler] = self.handlers[handler]()

        return recipe_urls, recipe_names
