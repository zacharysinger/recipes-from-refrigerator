"""
Flask app for recipes from refrigerator

NOTES:
- for all of the websites use the search function for ingredients and just have it be close enough, not exactly right

FIXES:
- I have to make the transition from when it grabs the data from the retriever to put into my html
            - actually grabbing the data from the recipe website is fast, but its the transfer from
            app.py to results.html that is really slow
"""
import ast
from flask import Flask, render_template, request
from models import Recipes, Engine
from retriever import Retriever
from sqlalchemy.orm import sessionmaker

APP = Flask(__name__)

DBSession = sessionmaker(bind=Engine)()


def result_handler():
    """
    Post handler for request data
    Adds request data into sqlite database
    First pulls data in database, but if request ingredients are not in database ingredients,
        pulls from request URL and adds to database
    """
    desired_handlers = ['allrecipes', 'foodnetwork', 'epicurious']
    user_ingredients = [request.form[task] for task in request.form]
    ingredients = []

    for i in sorted(user_ingredients):
        j = i.replace(' ', '')
        ingredients.append(j)

    exists = DBSession.query(Recipes).get(str(ingredients))

    if exists:
        ar_recipe_urls = ast.literal_eval(exists.ar_recipe_url)
        ar_recipe_names = ast.literal_eval(exists.ar_recipe_name)

        fn_recipe_urls = ast.literal_eval(exists.fn_recipe_url)
        fn_recipe_names = ast.literal_eval(exists.fn_recipe_name)

        ep_recipe_urls = ast.literal_eval(exists.ep_recipe_url)
        ep_recipe_names = ast.literal_eval(exists.ep_recipe_name)

    else:
        ar_recipe_links = list(Retriever(ingredients)(desired_handlers)[0]['allrecipes'])
        ar_recipe_urls = ar_recipe_links[0]
        ar_recipe_names = ar_recipe_links[1]

        fn_recipe_links = list(Retriever(ingredients)(desired_handlers)[0]['foodnetwork'])
        fn_recipe_urls = fn_recipe_links[0]
        fn_recipe_names = fn_recipe_links[1]

        ep_recipe_links = list(Retriever(ingredients)(desired_handlers)[0]['epicurious'])
        ep_recipe_urls = ep_recipe_links[0]
        ep_recipe_names = ep_recipe_links[1]

        ingredient_add = Recipes(ingredients=str(ingredients), ar_recipe_url=str(ar_recipe_urls),
                                 ar_recipe_name=str(ar_recipe_names), fn_recipe_url=str(fn_recipe_urls),
                                 fn_recipe_name=str(fn_recipe_names), ep_recipe_url=str(ep_recipe_urls),
                                 ep_recipe_name=str(ep_recipe_names))
        DBSession.add(ingredient_add)
        DBSession.commit()

    return ar_recipe_urls, ar_recipe_names, fn_recipe_urls, fn_recipe_names, ep_recipe_urls, ep_recipe_names


@APP.route('/', methods=['GET'])
def index():
    """
    User facing form flask method
    """
    return render_template('index.html')


@APP.route('/results', methods=['POST'])
def results():
    """
    Runs result_handler function
    """
    result = result_handler()
    ar_recipe_urls = result[0]
    ar_recipe_names = result[1]
    fn_recipe_urls = result[2]
    fn_recipe_names = result[3]
    ep_recipe_urls = result[4]
    ep_recipe_names = result[5]
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


@APP.route('/mobile', methods=['GET'])
def mobile():
    """
    Mobile Version
    User facing form flask method
    """
    return render_template('mobile.html')


@APP.route('/mobileResults', methods=['POST'])
def mobile_result_handler():
    """
    Mobile Version
    Runs result_handler function
    """
    result = result_handler()
    ar_recipe_urls = result[0]
    ar_recipe_names = result[1]
    fn_recipe_urls = result[2]
    fn_recipe_names = result[3]
    ep_recipe_urls = result[4]
    ep_recipe_names = result[5]
    return render_template('mobileResults.html', ar_recipe_urls=ar_recipe_urls, ar_urls_length=len(ar_recipe_urls),
                           ar_recipe_names=ar_recipe_names, fn_recipe_urls=fn_recipe_urls,
                           fn_urls_length=len(fn_recipe_urls), fn_recipe_names=fn_recipe_names,
                           ep_recipe_urls=ep_recipe_urls, ep_urls_length=len(ep_recipe_urls),
                           ep_recipe_names=ep_recipe_names)


@APP.route('/mobileRecipes', methods=['GET'])
def mobile_recipes():
    """
    Mobile Version
    Displays special recipes inputted by me
    Recipes by: _______
    """
    return render_template('mobileRecipes.html')


if __name__ == '__main__':
    APP.run(port='8080', host='127.0.0.1', debug=True)
