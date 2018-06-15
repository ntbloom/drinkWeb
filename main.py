#! usr/bin/env python3

from flask import Flask, render_template, request
import drinkFinder
import json

app = Flask(__name__)

included = []
excluded = []



@app.route('/results', methods=['POST'])
def printDrinks():
    incl = request.form['includedIngredients']
    if len(incl)>1:
        incl = incl.split(',')
        for i in incl:
            i = i.strip()
            included.append(i)
    # print('\n\n', 'included: ', included) # for debugging
    excl = request.form['excludedIngredients']
    if len(excl)>1:
        excl = excl.split(',')
        for i in excl:
            i = i.strip()
            excluded.append(i)
    # print('\n\n', 'excluded: ', excluded) # for debugging
    rawDrinks = list(drinkFinder.drinkSearch(included, excluded))
    master = []
    for drink in rawDrinks:
        drinks = {}
        drinks['name'] = drink
        ingredients = drinkFinder.getRecipe(drink)
        drinks['recipe'] = ingredients
        master.append(drinks)
    # print('master: ', master) #for debugging
    included.clear()
    excluded.clear()
    if len(master)==0:
        return render_template('resultsEmpty.html')
    else:
        return render_template('results.html', drinks=master, qty = len(master))

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def whoops(i):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('404.html'), 500

# for debugging
if __name__ == '__main__':
    app.run(port=5000, debug=True)
