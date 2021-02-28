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