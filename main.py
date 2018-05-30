#! usr/bin/env python3

from flask import Flask, render_template, request

app = Flask(__name__)

included = []
excluded = []

@app.route('/results', methods=['POST'])
def printDrinks():
    included = (request.form['includedIngredients'])
#TODO: insert drinkFinder app here
    return included

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)