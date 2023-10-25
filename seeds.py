#перероблений модуль з дз_08
import json
from models import Author, Quote
import connect

import configparser


config = configparser.ConfigParser()
config.read('config.ini')

qoutes_file = config.get('JS', 'qoutes_file')
authors_file = config.get('JS', 'authors_file')


def insert_author_in_db():
    with open(authors_file, 'r', encoding='utf-8') as author_file:
        author_data = json.load(author_file)

    for obj in author_data:
        author = Author(
            fullname=obj['fullname'],
            born_date=obj['born_date'],
            born_location=obj['born_location'],
            description=obj['description']
        )
        author.save()
        print(f'Author {author.fullname} added in db')


def insert_quotes_in_db():
    with open(qoutes_file, 'r', encoding='utf-8') as quote_file:
            quote_data = json.load(quote_file)

    for obj in quote_data:
        author = Author.objects(fullname=obj['author']).first()

        if author:
            quote = Quote(
                tags=obj['tags'],
                author=author,
                quote=obj['quote']
            )
            quote.save()
            print(f'Quote {author.fullname} added in db')
        else:
            print(f"Author '{obj['author']}' not found, skipping quote.")

if __name__ == "__main__":
     print("added data in db OK")