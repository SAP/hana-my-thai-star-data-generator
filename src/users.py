import random
import re
import csv
from os import path
from pprint import pprint

def generate_record(i, row, addresses):
    address = random.choice(addresses)
    return {
        'id': 1000 + i,
        'name': row[0] + ' ' + row[1],
        'username': row[0] + row[1],
        'password': row[0] + row[1],
        'email': row[0].lower() + '.' + row[1].lower() + '@mail.com',
        'street': address['street'],
        'housenumber': re.search(r'\d+', address['housenumber']).group(),
        'plz': address['plz'],
        'city': 'Heidelberg',
        'country': 'Deutschland',
        'geocode': address['geocode']
    }

def generate_data():
    file = open(path.join(path.dirname(path.dirname(__file__)), 'resources', 'names.csv'), newline='', encoding='utf-8')
    data = csv.reader(file, delimiter=',')
    names = list(data)[1:]

    file = open(path.join(path.dirname(path.dirname(__file__)), 'resources', 'heidelberg-buildings.csv'), newline='', encoding='utf-8')
    data = csv.reader(file, delimiter='\t')

    addresses = [
        {
            'plz': row[0],
            'street': row[1],
            'housenumber': row[2],
            'geocode': row[3]
        }
        for i, row in enumerate(data)
        if i >= 1
    ]

    return [
        generate_record(i, row, addresses)
        for (i, row) in enumerate(names)
    ]

if __name__ == '__main__':
    pprint(generate_data())
