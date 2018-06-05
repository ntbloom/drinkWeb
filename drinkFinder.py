#! usr/bin/env python3
# main.py -- file for executing drinkFinder searches in Flask app

import sqlite3, re

# connection to drinkBase.db
drinkBase = sqlite3.connect('static/drinkBase.db', check_same_thread=False)
drinkBase.row_factory = lambda cursor, row: row[0]
cursor = drinkBase.cursor()

# create drinkDictionary from SQL database
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
drinkNames = sorted(drinkDictionary.keys()) # a list of all drink names

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
    return possibleDrinks



# master search function called from webpage/Flask app
def drinkSearch(incIngredients, exclIngredients):
    '''master search algorithm'''
    drinks = set(drinkNames)
    if len(incIngredients)>0:
        for ingredient in incIngredients:
            included = ingredientRegex(ingredient)
            drinks = drinks & included
    print('\n\n', str(len(drinks)), 'drinks after inclusion loop: ', sorted(drinks), '\n\n') #for debugging only

    if len(exclIngredients)>1:
        for ingredient in exclIngredients:
            excluded = ingredientRegex(ingredient)
            print('excluded drinks: ', excluded) # for debugging only
            drinks = drinks - excluded

    # debugging exclusion loop
    print('length of excluded: ', len(exclIngredients))
    print('excluded ingredients: ', exclIngredients)
    print(len(drinks), ' drinks after excluded loop: ', sorted(drinks), '\n\n')

    drinks = sorted(drinks)
    return drinks



# printing recipe component
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
    recipe = str(recipe)
    return recipe

def printDrinks():
    for result in searchResults:
        print(result, '\n', getRecipe(result), '\n\n')


'''debugging steps'''

# # for testing ingredients
# includedIngredients = ['vermouth']
# excludedIngredients = ['rye']

# print('allDrinks: ', allDrinks, '\n')
# searchResults = sorted(drinkSearch(includedIngredients, excludedIngredients))
# print('searchResults: ', searchResults)
# print('\n\n vermouth regex: ', ingredientRegex('vermouth'))
# print('\n\n rye regex: ', ingredientRegex('rye'))
# testRun = drinkSearch(includedIngredients, excludedIngredients)
# print(testRun)

# # for getRecipe debugging
# newTest = getRecipe('Gimlet')
# print(newTest)
