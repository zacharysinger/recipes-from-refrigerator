"""
Flask app for recipes from refrigerator
"""

# for all of the websites use the search function for ingredients and just have it be close enough, not exactly right

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
    recipe_links = Retriever(ingredients)(desired_handlers)

    it = iter(recipe_links.values())

    ar_list_of_links, fn_list_of_links, ep_list_of_links = next(it), next(it), next(it)

    return render_template('results.html', ar_list_of_links=ar_list_of_links, ar_links_length=len(ar_list_of_links),
                           fn_list_of_links=fn_list_of_links, fn_links_length=len(fn_list_of_links),
                           ep_list_of_links=ep_list_of_links, ep_links_length=len(ep_list_of_links))


if __name__ == '__main__':
    APP.run(port='3600', host='127.0.0.1', debug=True)
