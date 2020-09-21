#Holiday data from https://www.feiertagskalender.ch/export.php?geo=3060&hl=en
#row[1] -> MESS_DATUM
#row[2] -> Designation

import csv
import datetime
from os import path

def get_holiday_data():
    result = []
    with open(path.join(path.dirname(path.dirname(__file__)), 'resources', 'holidays.csv'), 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            try:
                result += [{
                    'date': datetime.datetime.strptime(row[0], '%d.%m.%Y').date(),
                    'designation': row[1]
                }]
            except ValueError:
                pass

    return result
