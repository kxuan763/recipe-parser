import requests

from bs4 import BeautifulSoup

URL = 'https://www.allrecipes.com/recipe/93597'
page = requests.get(URL)

#print(page.content)

soup = BeautifulSoup(page.content, "lxml")
name = soup.find("h1", class_="headline").text
print(name)

print('ingredients')
ingredients = soup.find_all("span", class_="ingredients-item-name")
for i in ingredients:
    print(i.text.strip())

print('directions')
directions = soup.find_all("div", class_="paragraph")
for d in directions:
    print(d.text)