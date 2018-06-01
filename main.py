#! usr/bin/env python3

from flask import Flask, render_template, request
from static import drinkFinder

app = Flask(__name__)

included = []
excluded = []



@app.route('/', methods=['POST'])
def printDrinks():
    included = (request.form['includedIngredients'])
    excluded = (request.form['excludedIngredients'])
    possibleDrinks = drinkFinder.drinkSearch(included, excluded)
    return possibleDrinks

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)