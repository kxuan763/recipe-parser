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

# CORPORA
ALL_TOOLS = ['grill', 'whisk', 'pot', 'pan', 'dish', 'grater', 'knife', 'board', 'pin', 'skillet', 'griddle', 'blender', 'dish', 'sifter', 'strainer', 'mallet', 'bowl', 'oven', 'stove', 'sheet', 'masher', 'beater', 'wok', 'iron', 'ladle']
# For handling special two word tools
SPEC_TOOLS = ['dish', 'pan', 'pin', 'sheet', 'iron', 'board']
TOOL_PREF = ['baking', 'cookie', 'rolling', 'waffle', 'cutting']
# Methods
ALL_METHODS = ['refrigerate', 'toss', 'sprinkle', 'whisk', 'press', 'bake', 'saute', 'preheat', 'fry', 'boil', 'broil', 'chop', 'cut', 'mash', 'blend', 'tenderize', 'heat', 'preheat']
# Times
TIME_WORDS = ['minute', 'minutes', 'second', 'seconds', 'hour', 'hours']
# For vegetarian transformations
MEATS = ['chicken', 'duck', 'venison', 'rabbit', 'bison', 'goat', 'shrimp', 'clams', 'lobster', 'crab', 'beef', 'steak', 'pork', 'ham', 'turkey', 'fish', 'tuna', 'salmon', 'cod', 'lamb']
VEG_PROTEINS = ['tofu', 'beans', 'lentils', 'chickpeas']
# For healthy transformations
UNHEALTHY_ING = ['butter', 'sugar', 'salt', 'oil', 'cheese', 'dressing', 'ketchup', 'mayonnaise']
# Because fractions suck and so does allrecipes.com
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

# make_veg takes a parsed recipe dict and mutates it to replace meats with tofu
def make_veg(parsed_recipe):
    for step_no in parsed_recipe.keys():
        ingr = parsed_recipe[step_no]['ingredients']
        for j in range(len(ingr)):
            if any(MEAT in ingr[j] for MEAT in MEATS):
                ingr[j] = 'tofu'
                    #print(ingr)

# Same thing but other way around
def make_unveg(parsed_recipe):
    for step_no in parsed_recipe.keys():
        ingr = parsed_recipe[step_no]['ingredients']
        for j in range(len(ingr)):
            if any(prot in ingr[j] for prot in VEG_PROTEINS):
                ingr[j] = 'chicken'

# For make healthy, cut quantities of unhealthy ingredients by 1/2
# For make unhealthy, double such ingredients.
# Input is ingredient dict for a recipe
def make_healthy(ingredients):
    for ingredient in ingredients.keys():
        if any(unh in ingredient for unh in UNHEALTHY_ING):
            ingredients[ingredient][0] = ingredients[ingredient][0]/2

def make_unhealthy(ingredients):
    for ingredient in ingredients.keys():
        if any(unh in ingredient for unh in UNHEALTHY_ING):
            ingredients[ingredient][0] = ingredients[ingredient][0]*2






# test_strings = ['Bake the fish in a pan for 30 minutes!', 'Bring 2 cups of water to a boil in a large pot for 4 hours', 'Fry the chicken in the largest pan you have']


fractiondict = {'½':0.5, '⅓':0.333, '⅔': 0.667, '¼':0.25, '¾':0.75, '⅝':0.625, '⅛':0.125, '⅜':0.375, '⅞':0.875, '1 ½':1.5}

#list_of_ingredients = ['pineapple', 'bell pepper', 'carrot', 'onion', 'avocado','avocado oil', 'salt', 'pepper', 'chicken', 'water', 'cornstarch', 'brown sugar', 'rice vinegar', 'ketchup', 'soy sauce', 'chile-garlic sauce', 'ginger-garlic paste', 'white pepper']
measures = ['tablespoon', 'teaspoon', 'pound', 'cup', 'ounce']

beans_and_legumes = ['black bean', 'black-eyed pea', 'cannellini bean', 'chickpea', 'fava bean', 'great northern bean', 'kidney bean', 'lentil bean', 'lima bean', 'pinto bean', 'soybean', 'edamame', 'white bean']
meat_and_poultry = ['beef', 'chicken', 'wild game', 'goat', 'ham', 'lamb', 'pork', 'sausage', 'turkey']
wild_game = ['venison', 'elk', 'duck', 'goose', 'buffalo', 'bison', 'rabbit']
chocolate = ['chocolate', 'cocoa']
oil = ['coconut oil', 'olive oil', 'sesame oil', 'avocado oil', 'vegetable oil', 'canola oil', 'peanut oil']
dairy = ['cheese', 'butter', 'buttermilk', 'sour cream', 'egg']
extracts = ['vanilla extract', 'anise extract', 'peppermint extract', 'lemon extract', 'orange extract', 'butter extract', 'almond extract', 'maple extract', 'rum extract']
flours = ['white rice flour', 'tapioca flour', 'chickpea flour', 'almond meal', 'coconut flour', 'brown rice flour', 'soy flour', 'corn flour', 'oat flour']
fruit = ['apple', 'apricot', 'avocado', 'banana', 'berry', 'cranberry', 'blueberry', 'raspberry', 'strawberry', 'blackberry', 'cherry', 'citrus', 'lemon', 'orange', 'lime', 'grapefruit', 'coconut', 'dates', 'fig', 'fruit', 'grape', 'kiwi', 'mango', 'melon', 'watermelon', 'cantaloupe', 'honeydew', 'nectarine', 'papaya', 'peach', 'pear', 'persimmon', 'pineapple', 'plum', 'pomegranate', 'raisin', 'tamarind']
herbs = ['basil', 'bay leaves', 'bay leaf' 'chervil', 'chives', 'cilantro', 'dill', 'lemongrass', 'marjoram', 'dill', 'lemongrass', 'marjoram', 'mint', 'oregano', 'parsley', 'rosemary', 'sage', 'savory', 'tarragon', 'thyme', 'lavender', 'rose']
spices = ['allspice', 'anise', 'annatto', 'cajun', 'caraway', 'cardamom', 'celery seed', 'chili powder', 'cinnamon', 'cloves', 'coriander', 'cumin', 'curry', 'curry powder', 'fennel seed', 'fenugreek', 'garam masala', 'jerk spice', 'mace', 'mustard', 'nutmeg', 'paprika', 'pickling spice', 'poppy seed', 'cayenne pepper', 'saffron', 'sesame seed', 'turmeric', 'vanilla bean', 'white pepper', 'peppercorn', 'ginger', 'star anise']
mushrooms = ['chanterelle mushroom', 'crimini mushroom', 'enoki mushroom', 'morel mushroom', 'oyster mushroom', 'porcini mushroom', 'portobello mushroom', 'shiitake mushroom']
nuts_and_seeds = ['chia seed', 'peanut', 'peanut butter', 'pecan', 'almond', 'flax seed', 'walnut', 'amaranth']
shellfish = ['clam', 'crab', 'crawfish', 'lobster', 'mussel', 'octopus', 'squid', 'oyster', 'scallop', 'shrimp']
vegetables = ['artichoke', 'artichoke', 'asparagus', 'beet', 'bell pepper', 'bok choy', 'broccoli', 'brussels sprout', 'mushroom', 'green bean', 'corn', 'cucumber', 'eggplant', 'fennel', 'garlic', 'greens', 'green pea', 'pea', 'radish', 'rhubarb', 'sweet potato', 'tomato', 'tomatillo', 'nopales', 'turnip', 'snow pea', 'sugar snap pea', 'potato', 'squash', 'carrot', 'mixed vegetable', 'cauliflower', 'cabbage', 'leek', 'onion', 'parsnip', 'rutabaga', 'shallot', 'yam', 'water chestnut', 'jicama', 'okra', 'chile pepper', 'olive', 'celery root', 'celery']
grain = ['barley', 'rice', 'buckwheat', 'bulgur', 'cornmeal', 'millet', 'oat', 'quinoa', 'spelt']
misc = ['salt', 'black pepper', 'water', 'sugar', 'vinegar', ]
sauces = ['ketchup', 'mustard', 'soy sauce']

#todo: add sauces and other missing kitchen staples
#todo: find preparation/descriptor words

list_of_ingredients = beans_and_legumes + meat_and_poultry + wild_game + chocolate + oil + dairy + extracts + flours + fruit + herbs + spices + mushrooms + nuts_and_seeds + shellfish + vegetables + grain + misc


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
    if quantity == 0:
        quantity = ''  
    return {match: [quantity, measure, '']}


# ingredients structure: {ingredient name: [quantity, measurement, descriptors]}
    #tagged_tokens = nltk.pos_tag(tokens)
    #return tokens

# TESTING
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
#dummy_ing = {'pasta':[1,'cup',''],'chicken':[2,'breasts','chopped'], 'butter':[1,'tsp','melted'],'sugar':[3,'tsp',''], 'italian dressing':[3,'tsp','']}
# print(dummy_ing)
# make_healthy(dummy_ing)
# print(dummy_ing)
#recipe = extract_text(URL)
#parsed_recipe = parse_steps(recipe[2], ['soy sauce','italian-style dressing','chicken','butter','hot pepper sauce'])
#print(parsed_recipe)
#make_veg(parsed_recipe)
#print(parsed_recipe)
#make_unveg(parsed_recipe)
#print(parsed_recipe)




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