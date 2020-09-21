#Weather data from https://www.dwd.de/DE/leistungen/klimadatendeutschland/klarchivtagmonat.html
#row[1] -> MESS_DATUM
#row[13] -> TMK

import csv
import datetime
from os import path

def get_weather_data():
    result = []
    with open(path.join(path.dirname(path.dirname(__file__)), 'resources', 'weather.txt'), 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            try:
                result += [{
                    'date': datetime.datetime.strptime(row[1], "%Y%m%d").date(),
                    'temperature': float(row[13])
                }]
            except ValueError:
                pass

    return result
