#! usr/bin/env python3

from flask import Flask, render_template, request
import drinkFinder
import json

app = Flask(__name__)

included = []
excluded = []



@app.route('/results', methods=['POST'])
def printDrinks():
    included.insert(0, (request.form['includedIngredients']))
    # print('\n\n', 'included: ', included) # for debugging
    excluded.insert(0, (request.form['excludedIngredients']))
    # print('\n\n', 'excluded: ', excluded) # for debugging
    rawDrinks = list(drinkFinder.drinkSearch(included, excluded))
    drinks = {}
    for drink in rawDrinks:
        ingredients = drinkFinder.getRecipe(drink)
        drinks[drink] = ingredients

        # recipe = str((drink, ingredients))
        # drinks.append(recipe)
    # drinks = str(drinks)
    drinks = json.dumps(drinks)
    included.clear()
    excluded.clear()
    return drinks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html', drinks=printDrinks)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
