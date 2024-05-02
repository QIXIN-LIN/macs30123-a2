import os
import json
import requests
from bs4 import BeautifulSoup
import dataset
from datetime import datetime
import re

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
endpoint = os.getenv('DB_ENDPOINT')
port = os.getenv('DB_PORT')

db_url = \
    'mysql+mysqlconnector://{}:{}@{}:{}/books'.format(
        user,
        password,
        endpoint,
        port)

db = dataset.connect(db_url)


def scrape_book(html_soup, book_id):
    main = html_soup.find(class_='product_main')
    book = {}
    book['book_id'] = book_id
    book['title'] = main.find('h1').get_text(strip=True)
    book['price'] = main.find(class_='price_color').get_text(strip=True)
    book['stock'] = main.find(class_='availability').get_text(strip=True)
    book['rating'] = ' '.join(main.find(class_='star-rating') \
                        .get('class')).replace('star-rating', '').strip()
    book['img'] = html_soup.find(class_='thumbnail').find('img').get('src')
    desc = html_soup.find(id='product_description')
    book['description'] = ''
    if desc:
        book['description'] = desc.find_next_sibling('p') \
                                  .get_text(strip=True)
    book_product_table = html_soup.find(text='Product Information').find_next('table')
    for row in book_product_table.find_all('tr'):
        header = row.find('th').get_text(strip=True)
        # Since we'll use the header as a column, clean it a bit
        # to make sure SQLite will accept it
        header = re.sub('[^a-zA-Z]+', '_', header)
        value = row.find('td').get_text(strip=True)
        book[header] = value

    '''
    endpoint = os.getenv('DB_ENDPOINT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    port = os.getenv('DB_PORT')
    '''

    db['book_info'].upsert(book, ['book_id'])

    print("Data successfully inserted or updated.")


def lambda_handler(event, context):
    '''
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    endpoint = os.getenv('DB_ENDPOINT')
    port = os.getenv('DB_PORT')
    '''

    '''
    db_url = \
        'mysql+mysqlconnector://{}:{}@{}:{}/books'.format(
            user,
            password,
            endpoint,
            port)
    #db = dataset.connect(db_url)
    '''

    base_url = 'http://books.toscrape.com/'
    
    book_id = event['book_id']
    book_url = base_url + 'catalogue/{}'.format(book_id)
    # Fetch the page
    r = requests.get(book_url)
    r.encoding = 'utf-8'
    html_soup = BeautifulSoup(r.text, 'html.parser')

    # Scrape the book data

    scrape_book(html_soup, book_id)
    db['books'].upsert({'book_id' : book_id,
                        'last_seen' : datetime.now()
                        }, ['book_id'])
