import requests
from bs4 import BeautifulSoup
import json

import configparser


config = configparser.ConfigParser()
config.read('config.ini')

url_pars = config.get('URL', 'uri')
qoutes_file = config.get('URL', 'qoutes_file')

def parser_url(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')
    return quotes, authors, tags

def create_quotes_data(authors, quotes, tags) -> list:
    result = []
    for i in range(0, len(quotes)):
        tag = []
        quote = quotes[i].text
        author = authors[i].text
        tagsforquote = tags[i].find_all('a', class_='tag')
        for tagforquote in tagsforquote:
            tag.append(tagforquote.text)
        data_dict = {
            "tag": tag,
            "Author": author,
            "quote": quote            
            }
        result.append(data_dict)
    return result

def add_to_json(file: str, data: list):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        print(f'JSON-file {file} created')
    
# url = 'https://quotes.toscrape.com/'
# response = requests.get(url_pars)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('span', class_='text')
# authors = soup.find_all('small', class_='author')
# tags = soup.find_all('div', class_='tags')

# data_list = []
# for i in range(0, len(quotes)):
#     tag = []
#     print('+' * 10)
#     # print(quotes[i].text)
#     quote = quotes[i].text
#     # print('--' + authors[i].text)
#     author = authors[i].text
#     tagsforquote = tags[i].find_all('a', class_='tag')
#     for tagforquote in tagsforquote:
#         print(tagforquote.text)
#         tag.append(tagforquote.text)
#     data = {
#         "Author": author,
#         "quote": quote,
#         "tag": tag
#         }
#     data_list.append(data)
    # with open("quotes2.json", "w", encoding="utf-8") as fd:
    #     json.dump(data_list, fd, ensure_ascii=False)

# print(data_list)

if __name__ == "__main__":
    # response = requests.get(url_pars)
    # soup = BeautifulSoup(response.text, 'lxml')
    # quotes = soup.find_all('span', class_='text')
    # authors = soup.find_all('small', class_='author')
    # tags = soup.find_all('div', class_='tags')

    # main()
    q, a, t = parser_url(url_pars)
    data_for_json = create_quotes_data(a, q, t)
    add_to_json(qoutes_file, data_for_json)