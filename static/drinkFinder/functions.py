#! usr/bin/env python3
# functions.py functions for drinkFinder app

import sqlite3, re

# connection to drinkBase.db
drinkBase = sqlite3.connect('drinkBase.db')
drinkBase.row_factory = lambda cursor, row: row[0]
cursor = drinkBase.cursor()

# create drinkDictionary
drinkNames = []
drinkList = []
drinkDictionary = {} # list of all possible drinks
cursor.execute('SELECT name FROM ingredients GROUP BY name')
drinkList = []
drinkList = cursor.fetchall()
for name in drinkList:
    name = name,
    cursor.execute('SELECT ingredient FROM ingredients where name like ? GROUP BY ingredient', name)
    name = name[0]
    ingredientTuple = cursor.fetchall()
    drinkDictionary[name] = ingredientTuple
drinkNames = drinkDictionary.keys()  # a list of all drink names

def allDrinks():
    '''returns a list of all possible drinks'''
    return drinkNames

# regex function
def ingredientRegex(ingredient=''):
    '''populates a set of all drinks containing a given ingredient'''
    possibleDrinks = set()
    searchTermFixed = (r'\w*' + ingredient + r'\w*')
    searchTermRE = re.compile(searchTermFixed, re.IGNORECASE)
    for drink in drinkNames:
        ingredientList = drinkDictionary[drink]
        for ingredient in ingredientList:
            match = searchTermRE.search(ingredient)
            if match == None:
                continue
            else:
                possibleDrinks.add(drink)
    return (possibleDrinks)

def getRecipe(drinkName):
    '''looks up and returns recipe using SQL'''
    cursor.execute('SELECT ingredient FROM ingredients WHERE name = ?', (drinkName,))
    ingredientList = cursor.fetchall()
    recipe = {}
    for i in ingredientList:
        cursor.execute('SELECT amount FROM ingredients where name = ? AND ingredient = ?', (drinkName, i))
        amount = cursor.fetchall()
        cursor.execute('SELECT unit FROM ingredients where name = ? AND ingredient = ?', (drinkName, i))
        unit = cursor.fetchall()
        recipe[i] = str(amount[0]) + ' ' + unit[0]
    return recipe
