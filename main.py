import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = '...'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


# Добавление данных из json (Задание 3)
with open('test_data.json', 'r') as td:
    data = json.load(td)

for element in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[element.get('model')]
    session.add(model(id=element.get('pk'), **element.get('fields')))
session.commit()


# Извлечение данных из таблицы (Задание 2):
publisher_id = input('Введите id издания: ')

book_list = []
shop_list = []
price_list = []
date_list = []

subq = session.query(Publisher).filter(Publisher.id == publisher_id).subquery()
for c in session.query(Book).join(subq, subq.c.id == Book.id_publisher).all():
    book_list.append(c.title)
book_subq = session.query(Book).join(subq, subq.c.id == Book.id_publisher).subquery()
stock_subq = session.query(Stock).join(book_subq, book_subq.c.id == Stock.id_book).subquery()
shop_subq = session.query(Shop).join(stock_subq, Shop.id == stock_subq.c.id_shop).subquery()
for c in session.query(Shop).join(stock_subq, Shop.id == stock_subq.c.id_shop).all():
    shop_list.append(c.name)
sale_q = session.query(Sale).join(stock_subq, stock_subq.c.id == Sale.id_stock).all()
i = 0
for c in sale_q:
    price_list.append(c.price)
    date_list.append(c.date_sale)
    i += 1

# вывод данных на печать
k = 0
print('\n')
while k < i:
    book = book_list[k]
    shop = shop_list[k]
    price = price_list[k]
    date = date_list[k]
    print(f'{book}' + ' | ' + f'{shop}' + ' | ' + f'{price}' + ' | ' + f'{date}')
    k += 1

session.close()
