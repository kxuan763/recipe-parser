import requests

from bs4 import BeautifulSoup

import nltk

URL = 'https://www.allrecipes.com/recipe/17167/sicilian-spaghetti/'

def extract_text(url):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")
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

# Corpora
ALL_TOOLS = ['grill', 'whisk', 'pot', 'pan', 'dish', 'grater', 'knife', 'board', 'pin', 'skillet', 'griddle', 'blender', 'dish', 'sifter', 'strainer', 'mallet', 'bowl', 'oven', 'stove', 'sheet', 'masher', 'beater', 'wok', 'iron', 'ladle']
SPEC_TOOLS = ['dish', 'pan', 'pin', 'sheet', 'iron', 'board']
TOOL_PREF = ['baking', 'cookie', 'rolling', 'waffle', 'cutting']
ALL_METHODS = ['refrigerate', 'toss', 'sprinkle', 'whisk', 'press', 'bake', 'saute', 'preheat', 'fry', 'boil', 'broil', 'chop', 'cut', 'mash', 'blend', 'tenderize', 'heat', 'preheat']
TIME_WORDS = ['minute', 'minutes', 'second', 'seconds', 'hour', 'hours']
MEATS = ['chicken', 'beef', 'steak', 'pork', 'ham', 'turkey', 'fish', 'tuna', 'salmon', 'cod']
VEG_PROTEINS = ['tofu', 'beans', 'lentils', 'chickpeas']
UNHEALTHY_ING = ['butter', 'sugar', 'salt', 'oil', 'cheese', 'dressing', 'ketchup', 'mayonnaise']

fractiondict = {'½':0.5, '⅓':0.333, '⅔': 0.667, '¼':0.25, '¾':0.75, '⅝':0.625, '⅛':0.125, '⅜':0.375, '⅞':0.875, '1 ½':1.5}

# regex all search conditions


# parse_steps calls parse_step on all text in list of steps and returns a dictionary of all steps
def parse_steps(steps, ingredients):
    # Steps dictionary
    # Key is step number, value is another dictionary with key strings ingredients, tools, methods, time
    # Sub dictionary values are lists of strings returned by parse_step
    stepdict = {}
    for i in range(len(steps)):
        stepdict[i+1] = parse_step(steps[i], ingredients)
    return stepdict





# parse_step(str:text, listof str:ingredients) -> tools:listof str, methods:listof str, times: listof str
def parse_step(text, ingredients):

    # Initialize
    text = text.lower()
    step = {}
    step['ingredients'] = []
    step['tools'] = []
    step['methods'] = []
    step['times'] = []

    # Tokenize and tag text using nltk
    tokens = nltk.word_tokenize(text)
    
    # Check verbs for methods and nouns for tools 
    # (can later add ability to check for ingredients once ingr list is made)
    
    for i in range(len(tokens)):
        
        word = tokens[i]

        if word in ALL_TOOLS:
            if word in SPEC_TOOLS and tokens[i-1] in TOOL_PREF:
                step['tools'].append(tokens[i-1] + ' ' + word)
            else:
                step['tools'].append(word)
        if word in TIME_WORDS:
            step['times'].append(tokens[i-1] + ' ' + word)
        if word in ingredients:
            step['ingredients'].append(word)
        if word in ALL_METHODS:
            step['methods'].append(word)
    
    return step

# make_veg takes a parsed recipe dict and returns 
# a copy with meats replaced with tofu
def make_veg(parsed_recipe):
    recipe_copy = parsed_recipe.copy()
    for step_no in recipe_copy.keys():
        ingr = recipe_copy[step_no]['ingredients']
        for j in range(len(ingr)):
            if ingr[j] in MEATS:
                ingr[j] = 'tofu'
                    #print(ingr)
    return recipe_copy

# Same thing but other way around
def make_unveg(parsed_recipe):
    recipe_copy = parsed_recipe.copy()
    for step_no in recipe_copy.keys():
        ingr = recipe_copy[step_no]['ingredients']
        for j in range(len(ingr)):
            if ingr[j] in VEG_PROTEINS:
                ingr[j] = 'chicken'
    return recipe_copy

# For make healthy, cut quantities of unhealthy ingredients by 1/2
# For make unhealthy, double such ingredients.





# test_strings = ['Bake the fish in a pan for 30 minutes!', 'Bring 2 cups of water to a boil in a large pot for 4 hours', 'Fry the chicken in the largest pan you have']

#URL = 'https://www.allrecipes.com/recipe/213068/grill-master-chicken-wings/?internalSource=hub%20recipe&referringContentType=Search'

def parse_ingredient(ingredient):
    tokens = nltk.word_tokenize(ingredient)
    #tagged_tokens = nltk.pos_tag(tokens)
    return tokens

# for test_string in test_strings:
#     print(parse_step(test_string))
recipe = extract_text(URL)
# parsed_recipe = parse_steps(recipe[2], ['soy sauce','italian-style dressing','chicken','butter','hot pepper sauce'])
# veg_recipe = make_veg(parsed_recipe)
# unveg_recipe = make_unveg(veg_recipe)
# print(veg_recipe,unveg_recipe)



# VEGETARIAN SUBSTITUTION LOGIC, DO NOT DELETE
""" for i in recipe[1]:
    # print(parse_ingredient(i))
    if any(MEAT in i for MEAT in MEATS):
        print(i, 'MEAT')
        tokens = parse_ingredient(i)
        for j in range(len(tokens)):
            if tokens[j] in MEATS:
                tokens[j] = 'tofu'
        print(tokens)

for i in recipe[1]:
    if any(protein in i for protein in VEG_PROTEINS):
        print(i, 'PROTEIN')
        tokens = parse_ingredient(i)
        for j in range(len(tokens)):
            if tokens[j] in VEG_PROTEINS:
                tokens[j] = 'chicken'
        print(tokens) """

# TO DO
# Doubling and halving quantities
# Unhealthy to healthy
# 
