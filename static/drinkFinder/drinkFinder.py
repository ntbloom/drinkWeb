#! usr/bin/env python3
# main.py -- file for executing drinkFinder searches

'''This is the text-based version of drinkFinder.

This file creates the basic framework to be later plugged into a GUI or web app.

How to use this search function in the command line:
    1) update lists on lines 15-22 with included, optional and excluded ingredients

'''

import functions

includedIngredients = ['gin']
excludedIngredients = ['lime']
allDrinks = functions.allDrinks()

def drinkSearch(includedIngredients, excludedIngredients):
    '''master search algorithm'''
    drinks = set(allDrinks)
    if len(includedIngredients)>0:
        for ingredient in includedIngredients:
            included = functions.ingredientRegex(ingredient)
            drinks = drinks & included
    print('\n\n', 'drinks after inclusion loop: ', sorted(drinks), '\n\n') #for debugging only

    if len(excludedIngredients)>0:
        for ingredient in excludedIngredients:
            excluded = functions.ingredientRegex(ingredient)
            drinks = drinks - excluded
    print('drinks after excluded loop: ', sorted(drinks), '\n\n') #for debugging only

    drinks = list(drinks)
    return sorted(drinks)


searchResults = sorted(drinkSearch(includedIngredients, excludedIngredients))
print('searchResults: ', searchResults) #for debugging only

def printDrinks():
    for result in searchResults:
        print(result, '\n', functions.getRecipe(result), '\n\n')

