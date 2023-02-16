import json
from pprint import pprint

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
    pprint(data)

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

session.close()
