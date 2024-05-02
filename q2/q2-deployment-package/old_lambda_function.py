import os
import json
import requests
from bs4 import BeautifulSoup
import mysql.connector
import dataset

def lambda_handler(event, context):
    #url = event['url']
    endpoint=os.getenv('DB_ENDPOINT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT'), 

    db_url = \
        'mysql+mysqlconnector://{}:{}@{}:{}/books'.format(
            endpoint,
            user,
            password,
            port)
    db = dataset.connect(db_url)

    base_url = 'http://books.toscrape.com/'
    book_id = event['book_id']
    book_url = base_url + 'catalogue/{}'.format(book_id)
    # Fetch the page
    r = requests.get(book_url)
    r.encoding = 'utf-8'
    html_soup = BeautifulSoup(r.text, 'html.parser')

    # Scrape the book data
    scrape_book(html_soup, book_id)



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
    db['book_info'].upsert(book, ['book_id'])
    main = html_soup.find(class_='product_main')
    book = {
        'book_id': book_id,
        'title': main.find('h1').get_text(strip=True),
        'price': main.find(class_='price_color').get_text(strip=True),
        'stock': main.find(class_='availability').get_text(strip=True),
        'rating': ' '.join(main.find(class_='star-rating').get('class')).replace('star-rating', '').strip(),
        'img': html_soup.find(class_='thumbnail').find('img').get('src'),
        'description': html_soup.find(id='product_description').find_next_sibling('p').get_text(strip=True) if html_soup.find(id='product_description') else ''
    }


def save_to_rds(book):
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
            PORT=os.getenv(DB_PORT, '3306'), 
        )
        cursor = conn.cursor()
        # Insert or update book data
        
        insert_query = """
        INSERT INTO books_table (
            book_id, title, price, stock, rating, img, description, UPC, Product_Type,
            Price_excl_tax, Price_incl_tax, Tax, Availability, Number_of_reviews
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            title=VALUES(title),
            price=VALUES(price),
            stock=VALUES(stock),
            rating=VALUES(rating),
            img=VALUES(img),
            description=VALUES(description),
            UPC=VALUES(UPC),
            Product_Type=VALUES(Product_Type),
            Price_excl_tax=VALUES(Price_excl_tax),
            Price_incl_tax=VALUES(Price_incl_tax),
            Tax=VALUES(Tax),
            Availability=VALUES(Availability),
            Number_of_reviews=VALUES(Number_of_reviews);
        """

        book_data = (
            'book_id_value', 'title_value', 'price_value', 'stock_value', 'rating_value', 'img_url', 'description_text',
            'UPC_code', 'product_type', 'price_excl_tax', 'price_incl_tax', 'tax_value', 'availability_status', 'number_of_reviews'
        )
        cursor.execute(insert_query, book_data)
        conn.commit()
        print("Data successfully inserted or updated.")
    
    except Exception as e:
        print("Error:", e)

    finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

