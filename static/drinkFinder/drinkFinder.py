#! usr/bin/env python3
# main.py -- file for executing drinkFinder searches

'''This is the text-based version of drinkFinder.

This file creates the basic framework to be later plugged into a GUI or web app.

How to use this search function in the command line:
    1) update lists on lines 15-22 with included, optional and excluded ingredients

'''

import functions

includedIngredients = []
optionalIngredients = []
excludedIngredients = []
allDrinks = functions.allDrinks()


def drinkSearch(includedIngredients, optionalIngredients, excludedIngredients):
    '''master search algorithm'''
    drinks = set(allDrinks)
    for ingredient in includedIngredients:
        included = functions.ingredientRegex(ingredient)
        drinks = drinks & included
    # print("drinks after inclusion loop: ", drinks, "\n\n")    #for testing only

    includedIngredients.pop()   # removes empty string from input() function, delete for web app
    if len(includedIngredients)==0:
        drinks = set(allDrinks)

    for ingredient in optionalIngredients:
        optional = functions.ingredientRegex(ingredient)
        options = drinks | optional
    # print("drinks after optional loop: ", drinks, "\n\n")  # for testing only


    optionalIngredients.pop()   # removes empty string from input() function, delete for web app
    if len(optionalIngredients)>0:
        drinks = options | drinks

    for ingredient in excludedIngredients:
        excluded = functions.ingredientRegex(ingredient)
        exclusions = drinks - excluded
        # print("drinks after excluded loop: ", drinks) #for testing only

    excludedIngredients.pop()   # removes empty string from input() function, delete for web app
    if len(excludedIngredients)>0:
        drinks = drinks - exclusions

    drinks = list(drinks)
    return drinks


searchResults = sorted(drinkSearch(includedIngredients, optionalIngredients, excludedIngredients))

def printDrinks():
    for result in searchResults:
        print(result, '\n', functions.getRecipe(result), '\n\n')