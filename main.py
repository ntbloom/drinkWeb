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
    print('\n\n', 'included: ', included) # for debugging
    excluded.insert(0, (request.form['excludedIngredients']))
    print('\n\n', 'excluded: ', excluded) # for debugging
    rawDrinks = list(drinkFinder.drinkSearch(included, excluded))
    master = []
    for drink in rawDrinks:
        drinks = {}
        drinks['name'] = drink
        ingredients = drinkFinder.getRecipe(drink)
        drinks['recipe'] = ingredients
        master.append(drinks)
    print('master: ', master)
    included.clear()
    excluded.clear()
    return render_template('results.html', drinks=master, qty = len(master))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
