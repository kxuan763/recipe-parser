import nltk
import json
import random
from statistics import mode
from collections import Counter
import itertools
import operator
from nltk.tokenize.treebank import TreebankWordDetokenizer

def makeDataStructure(string):
	amount=[]
	ingredient=[]
	tokenized = nltk.word_tokenize(string)

	for x in range(2):
		amount.append(tokenized[x])

	detokenized = TreebankWordDetokenizer().detokenize(tokenized[2:len(tokenized)])
	ingredient.append(detokenized)
	ingredient.append(amount)
	
	print(ingredient)

makeDataStructure("2 cups brown sugar")

FISH = ['salmon', 'cod', 'herring', 'mahi-mahi', 'mackerel', 'perch', 'rainbow trout', 'trout', 'sardines', 'bass',
		'striped bass', 'tuna', 'shark', 'swordfish', 'grouper', 'haddock', 'halibut', 'mahi', 'albacore', 'carp',
		'monkfish', 'snapper', 'sole', 'trout', 'rockfish', 'mullet', 'whitefish', 'saltfish', 'marlin', 'kingfish',
		'torsk', 'bonito']

SAUCES = ['alfredo', 'alfredo sauce', 'chutney', 'mayonnaise', 'soy sauce', 'barbecue sauce',
		'mushroom sauce', 'hot sauce', 'peanut sauce', 'hollandaise sauce', 'tomato sauce',
		'pesto', 'agrodolce sauce', 'agrodolce', 'tkemali', 'tkemali sauce', 'tartar', 'tartar sauce',
		'marie rose', 'marie rose sauce', 'demi-glace', 'demi-glace sauce', 'salsa', 'gravy', 'steak sauce',
		'cocktail sauce', 'red sauce', 'white sauce', 'chimichurri', 'marinara', 'marinara sauce',
		'worcestershire sauce', 'worcestershire', 'ketchup', 'mustard', 'hummus', 'tzatziki', 'ragu',
		'teriyaki', 'tahini', 'aioli', 'checca', 'checca sauce', 'amatriciana', 'amatriciana sauce', 'guacamole',
		'fish sauce', 'duck sauce', 'sweet and sour sauce']