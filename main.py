#! usr/bin/env python3

from flask import Flask, render_template, request
import drinkFinder

app = Flask(__name__)

included = []
excluded = []



@app.route('/', methods=['POST'])
def printDrinks():
    included = list((request.form['includedIngredients']))
    print('included: ', included)
    excluded = list((request.form['excludedIngredients']))
    print('excluded: ', excluded)
    return str(drinkFinder.drinkSearch(included, excluded))
    included.clear()
    excluded.clear()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)