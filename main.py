#! usr/bin/env python3

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/printDrinks', methods=['POST'])
def printDrinks():
    return (request.form['includedIngredients'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)