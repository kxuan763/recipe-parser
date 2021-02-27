import nltk

# Lists of tools and methods to look for in text
ALL_TOOLS = ['pot', 'pan', 'dish', 'grater', 'knife', 'cutting board', 'rolling pin', 'skillet', 'griddle', 'blender', 'baking dish', 'sifter', 'strainer', 'mallet', 'bowl', 'oven', 'stove', 'cookie sheet', 'baking sheet', 'masher', 'beater', 'casserole dish', 'wok', 'waffle iron', 'ladle']
ALL_METHODS = ['bake', 'saute', 'fry', 'boil', 'broil', 'chop', 'cut', 'mash', 'blend', 'tenderize']
TIME_WORDS = ['minute', 'minutes', 'second', 'seconds', 'hour', 'hours']
# add ingredients too


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


# for test_string in test_strings:
#     print(parse_step(test_string))





