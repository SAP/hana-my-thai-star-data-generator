from os import path
from itertools import chain
import xml.etree.ElementTree as ET
import csv

streets = []
unknownBuildings = []

def find_plz(postcode, street, housenumber):
    if postcode != None and len(postcode) > 0:
        streets.append({'street': street, 'plz': postcode[0].attrib['v']})
        return postcode[0].attrib['v']
    else:
        for str in streets:
            if str['street'] == street:
                return str['plz']

        if postcode != None:
            unknownBuildings.append({'street': street, 'plz': None, 'housenumber': housenumber})

    return None

def address_generate(postal_codes):
    print('Extracting addresses...')

    tree = ET.parse(path.join(path.dirname(__file__), '..', 'resources', 'addresses.xml'))
    ways = chain(tree.getroot().findall('way'), tree.getroot().findall('node'))

    with open(path.join(path.dirname(__file__), '..', 'resources', 'heidelberg-buildings.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['PLZ', 'Strasse', 'Hausnummer'])

        for way in ways:
            street = way.findall("./tag[@k='addr:street']")
            housenumber = way.findall("./tag[@k='addr:housenumber']")
            postcode = way.findall("./tag[@k='addr:postcode']")

            if len(street) > 0 and len(housenumber) > 0:
                if len(postcode) > 0 and postcode[0].attrib['v'] not in postal_codes:
                    continue

                plz = find_plz(postcode, street[0].attrib['v'], housenumber[0].attrib['v'])

                if plz != None and plz in postal_codes:
                    writer.writerow([plz, street[0].attrib['v'], housenumber[0].attrib['v']])

        for building in unknownBuildings:
            plz = find_plz(None, building['street'], building['housenumber'])

            if plz != None and plz in postal_codes:
                writer.writerow([plz, building['street'], building['housenumber']])

    print('Finished.')

address_generate(['69115', '69117', '69118', '69120', '69121', '69123', '69124', '69126'])
