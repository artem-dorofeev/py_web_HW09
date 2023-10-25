import requests
# from pprint import pprint
from bs4 import BeautifulSoup
import json

from models import Author, Quote
import configparser
from seeds import insert_author_in_db, insert_quotes_in_db


config = configparser.ConfigParser()
config.read('config.ini')

url_pars = config.get('URL', 'uri')
qoutes_file = config.get('JS', 'qoutes_file')
authors_file = config.get('JS', 'authors_file')


# парсимо вебсторінку
def parser_url(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')
    authors_link = soup.select('span > a')
    
    list_authors_urls = []
    for link in authors_link:
        if 'author' in link["href"]:
            list_authors_urls.append(url_pars+link['href'].removeprefix('/'))
    print(f'parsing url {url} it`s OK')
    return quotes, authors, tags, list_authors_urls


# обробляємо парсинг головної сторінки та кладемо у список словників потім це буде qoutes.json
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
            "tags": tag,
            "author": author,
            "quote": quote            
            }
        result.append(data_dict)
    print(f'create quotes data is OK')
    return result


# парсимо сторінки авторів та кладемо у список словників потім це буде authors.json
def create_authors_data(uri: list) -> list:
    result = []
    for link in uri:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        author_fullname = soup.find('h3', class_='author-title')
        born_date = soup.find('span', class_='author-born-date')
        born_location = soup.find('span', class_='author-born-location')
        description = soup.find('div', class_='author-description')

        data_dict = {
            'fullname': author_fullname.text,
            'born_date': born_date.text,
            'born_location': born_location.text,
            'description' : description.text.strip()[:50]          
            }
        result.append(data_dict)
    print(f'create authors data is OK')
    return result


# додаємо у json файл
def add_to_json(file: str, data: list):
    
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        print(f'JSON-file {file} created')
    


if __name__ == "__main__":

    q, a, t, a_l = parser_url(url_pars)
    quotes_for_json = create_quotes_data(a, q, t)
    authors_for_json = create_authors_data(a_l)
    add_to_json(qoutes_file, quotes_for_json)
    add_to_json(authors_file, authors_for_json)
    insert_author_in_db()
    insert_quotes_in_db()
    

