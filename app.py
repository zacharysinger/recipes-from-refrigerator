"""
Flask app for recipes from refrigerator

NOTES:
- for all of the websites use the search function for ingredients and just have it be close enough, not exactly right

FIXES:
- I have to make the transition from when it grabs the data from the retriever to put into my html
            - actually grabbing the data from the recipe website is fast, but its the transfer from
            app.py to results.html that is really slow
"""
from flask import Flask, render_template, request
from retriever import Retriever

APP = Flask(__name__)
LOGGER = APP.logger


@APP.route('/', methods=['GET'])
def index():
    """
    User facing form flask method
    """
    return render_template('index.html')


@APP.route('/results', methods=['POST'])
def result_handler():
    """
    Post handler for request data
    """
    desired_handlers = ['allrecipes', 'foodnetwork', 'epicurious']
    ingredients = [request.form[task] for task in request.form]

    ar_recipe_links = list(Retriever(ingredients)(desired_handlers)[0]['allrecipes'])
    ar_recipe_urls = [i for i in ar_recipe_links[0]]
    ar_recipe_names = [i for i in ar_recipe_links[1]]

    fn_recipe_links = list(Retriever(ingredients)(desired_handlers)[0]['foodnetwork'])
    fn_recipe_urls = [i for i in fn_recipe_links[0]]
    fn_recipe_names = [i for i in fn_recipe_links[1]]

    ep_recipe_links = list(Retriever(ingredients)(desired_handlers)[0]['epicurious'])
    ep_recipe_urls = [i for i in ep_recipe_links[0]]
    ep_recipe_names = [i for i in ep_recipe_links[1]]

    return render_template('results.html', ar_recipe_urls=ar_recipe_urls, ar_urls_length=len(ar_recipe_urls),
                           ar_recipe_names=ar_recipe_names, fn_recipe_urls=fn_recipe_urls,
                           fn_urls_length=len(fn_recipe_urls), fn_recipe_names=fn_recipe_names,
                           ep_recipe_urls=ep_recipe_urls, ep_urls_length=len(ep_recipe_urls),
                           ep_recipe_names=ep_recipe_names)


@APP.route('/recipes', methods=['GET'])
def recipes():
    """
    Displays special recipes inputted by me
    Recipes by: _______
    """
    return render_template('recipes.html')


if __name__ == '__main__':
    APP.run(port='3600', host='127.0.0.1', debug=True)
