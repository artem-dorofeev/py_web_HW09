import requests
from bs4 import BeautifulSoup
import json


url = 'https://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')

data_list = []
for i in range(0, len(quotes)):
    tag = []
    print('+' * 10)
    # print(quotes[i].text)
    quote = quotes[i].text
    # print('--' + authors[i].text)
    author = authors[i].text
    tagsforquote = tags[i].find_all('a', class_='tag')
    for tagforquote in tagsforquote:
        print(tagforquote.text)
        tag.append(tagforquote.text)
    data = {
        "Author": author,
        "quote": quote,
        "tag": tag
        }
    data_list.append(data)
    with open("quotes1.json", "w", encoding="utf-8") as fd:
        json.dump(data_list, fd, ensure_ascii=False)

print(data_list)