import requests

from bs4 import BeautifulSoup

import nltk

URL = 'https://www.allrecipes.com/recipe/17167/sicilian-spaghetti/'
URL = 'https://www.allrecipes.com/recipe/279987/'

def load_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    return soup

def extract_text(soup):
    name = soup.find("h1", class_="headline").text
    #print(name)

    #print('ingredients')
    list_i = []
    ingredients = soup.find_all("span", class_="ingredients-item-name")
    for i in ingredients:
        list_i.append(i.text.strip())
        #print(i.text.strip())
    
    #print('directions')
    list_d = []
    directions = soup.find_all("div", class_="paragraph")
    for d in directions:
        list_d.append(d.text)
        #print(d.text)

    return(name, list_i, list_d)

# 
# Lists of tools and methods to look for in text
ALL_TOOLS = ['pot', 'pan', 'dish', 'grater', 'knife', 'cutting board', 'rolling pin', 'skillet', 'griddle', 'blender', 'baking dish', 'sifter', 'strainer', 'mallet', 'bowl', 'oven', 'stove', 'cookie sheet', 'baking sheet', 'masher', 'beater', 'casserole dish', 'wok', 'waffle iron', 'ladle']
ALL_METHODS = ['bake', 'saute', 'fry', 'boil', 'broil', 'chop', 'cut', 'mash', 'blend', 'tenderize', 'heat']
TIME_WORDS = ['minute', 'minutes', 'second', 'seconds', 'hour', 'hours']

# regex all search conditions

# parse_step(str:text) -> tools:listof str, methods:listof str, times: listof str
def parse_step(text):

    # Initialize
    text = text.lower()
    tools = []
    methods = []
    times = []

    # Tokenize and tag text using nltk
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    
    # Check verbs for methods and nouns for tools 
    # (can later add ability to check for ingredients once ingr list is made)
    
    for i in range(len(tagged)):
        
        word = tagged[i][0]
        tag = tagged[i][1]
        # print(word, tag)

        # Check if noun (tools and ingredients)
        if tag == 'NN' or tag == 'NNS':
            if word in ALL_TOOLS:
                tools.append(word)
            if word in TIME_WORDS:
                times.append(tagged[i-1][0] + ' ' + word)

        # Check if verb (methods)
        if tag == 'VB' or tag == 'VBP' or tag == 'VBG':
            if word in ALL_METHODS:
                methods.append(word)
            elif word == 'bring':
                if 'boil' in text:
                    methods.append('boil')
    
    return tools, methods, times

# test_strings = ['Bake the fish in a pan for 30 minutes!', 'Bring 2 cups of water to a boil in a large pot for 4 hours', 'Fry the chicken in the largest pan you have']

fractiondict = {'½':0.5, '⅓':0.333, '⅔': 0.667, '¼':0.25, '¾':0.75, '⅝':0.625, '⅛':0.125, '⅜':0.375, '⅞':0.875, '1 ½':1.5}

list_of_ingredients = ['pineapple', 'bell pepper', 'carrot', 'onion', 'avocado','avocado oil', 'salt', 'pepper', 'chicken', 'water', 'cornstarch', 'brown sugar', 'rice vinegar', 'ketchup', 'soy sauce', 'chile-garlic sauce', 'ginger-garlic paste', 'white pepper']
measures = ['tablespoon', 'teaspoon', 'pound', 'cup', 'ounce']

# need to integrate into extract_text
def parse_ingredients(ingredients):
    list_ingredient = []
    for i in ingredients:
        list_ingredient.append(parse_ingredient(i))
    return list_ingredient

def parse_ingredient(ingredient):
    # ingredient name
    length = 0
    match = ''
    for i in list_of_ingredients:
        if i in ingredient:
            if len(i) > length:
                match = i
                length = len(i)
    # measure
    measure = ''
    for m in measures:
        if m in ingredient:
            measure = m
    # quantity
    quantity = 0
    tokens = nltk.word_tokenize(ingredient)
    for t in tokens:
        if t in fractiondict:
            quantity += fractiondict[t]
        elif t.isnumeric():
            quantity += int(t)     
    return {match: [measure, quantity]}


# ingredients structure: {ingredient name: [quantity, measurement, descriptors]}

# for test_string in test_strings:
#     print(parse_step(test_string))
#recipe = extract_text(URL)
""" for s in recipe[2]:
    print(s)
    print(parse_step(s)) """

p = load_page(URL)
recipe = extract_text(p)
print(recipe[1])
print(parse_ingredients(recipe[1]))
