# Helpful Links:
#   https://nycdatascience.com/blog/student-works/recipes-scraping-top-20-recipes-allrecipes/
#
# Note: Ingredients are at checklist__line underneath list-ingredients-1 and list-ingredients-2 for the class of the ul
# also should probably add a limit of how many links can be added to the website
# when adding all the recipe dat to database order by stars and reviews so we can have a max number of links

# download jquery and other files to be in scripts so its much faster

# use heroku for servers for free, or AWS free tier

# for sql alchemy store the ingredients of the recipe and the link to the recipe in a table in database


import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, url_for, redirect, make_response, Blueprint, session

from flask import current_app as app

import json

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/')
def form():
    return redirect(url_for('index'))


@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    # from flask import session, using cookies instead of global variables
    # possibly memoize that
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':

        ingredients = []

        list_of_links = []

        jsdata = request.form['canvas_data']

        user_input = json.loads(jsdata)

        print(user_input)

        new_input = []

        for counter in range(0, 5):
            r = requests.get("https://www.allrecipes.com/recipe/" + str(counter))

            soup = BeautifulSoup(r.text, "html.parser")

            for product in soup.find_all("span", "recipe-ingred_txt added"):
                ingredient = product.text.strip()

                ingredients.append(ingredient)

            for x in user_input:  # make this more efficient
                for y in ingredients:
                    if x in y:
                        new_input.append(x)

            if len(new_input) == len(ingredients) and len(ingredients) != 0 and len(new_input) != 0:
                new_link = "https://www.allrecipes.com/recipe/" + str(counter)
                list_of_links.append(new_link)
                counter += 1

            else:
                counter += 1

        session['links_length'] = len(list_of_links)

        session['list_of_links'] = list_of_links

        session['ingredients_length'] = len(ingredients)

        session['ingredients'] = ingredients

        session['user_input_length'] = len(user_input)

        session['user_input'] = user_input

    return render_template('results.html')


@main_bp.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        return render_template('results.html', links_length=session['links_length'],
                               list_of_links=session['list_of_links'], ingredients_length=session['ingredients_length'],
                               ingredients=session['ingredients'], user_input_length=session['user_input_length'],
                               user_input=session['user_input'])


# if __name__ == '__main__':
#     app.run(port='3600', host='127.0.0.1', debug=True)
