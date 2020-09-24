from os import path
from itertools import chain
import xml.etree.ElementTree as ET
import csv
import configparser

streets = []
unknownBuildings = []

def find_plz(postcode, street, housenumber, geocode):
    if postcode != None and len(postcode) > 0:
        streets.append({'street': street, 'plz': postcode[0].attrib['v'], 'geocode': geocode})
        return postcode[0].attrib['v']
    else:
        for str in streets:
            if str['street'] == street:
                return str['plz']

        if postcode != None:
            unknownBuildings.append({'street': street, 'plz': None, 'housenumber': housenumber, 'geocode': geocode})

    return None

def find_coordinates(nodeDict, node_id):
    node = nodeDict[node_id]
    if node is None:
        return {'nodeId' : node_id, 'lat': None, 'lon': None}

    return {'nodeId' : node_id, 'lat': node.attrib.get('lat'), 'lon': node.attrib.get('lon')}


def address_generate(postal_codes):
    print('Extracting addresses...')

    config = configparser.ConfigParser()
    config.read(path.join(path.dirname(path.dirname(__file__)), 'config.ini'))

    isHANAExpress = config.getboolean('hana', 'express_edition', fallback=False)

    tree = ET.parse(path.join(path.dirname(path.dirname(__file__)), 'resources', 'addresses.xml'))
    nodes = tree.getroot().findall('node')
    ways = chain(tree.getroot().findall('way'), nodes)
    nodeDict = {}

    if isHANAExpress:
        for node in nodes:
            node_id = node.attrib.get('id')
            if node_id is None:
                continue
            nodeDict[node_id] = node

    with open(path.join(path.dirname(path.dirname(__file__)), 'resources', 'heidelberg-buildings.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['PLZ', 'Strasse', 'Hausnummer', 'Geocode'])

        for way in ways:
            street = way.findall("./tag[@k='addr:street']")
            housenumber = way.findall("./tag[@k='addr:housenumber']")
            postcode = way.findall("./tag[@k='addr:postcode']")
            geocode = None

            if isHANAExpress:
                lat = way.attrib.get('lat')
                lon = way.attrib.get('lon')
                if lat is None or lon is None:
                    nodes = way.findall("./nd")
                    if len(nodes) == 0:
                        pass
                    elif len(nodes) == 1:
                        node_id = nodes[0].attrib.get('ref')
                        coordinates = find_coordinates(nodeDict, node_id)
                        lat = coordinates['lat']
                        lon = coordinates['lon']
                        geocode = 'POINT(' + lon + ' ' + lat + ')'
                    elif len(nodes) == 2:
                        node_id = nodes[0].attrib.get('ref')
                        coordinates = find_coordinates(nodeDict, node_id)
                        lat = coordinates['lat']
                        lon = coordinates['lon']
                        geocode = 'POINT(' + lon + ' ' + lat + ')'
                    else:
                        geocode = 'POLYGON(('
                        for node in nodes:
                            if len(geocode) > len('POLYGON(('):
                                geocode += ','
                            node_id = node.attrib.get('ref')
                            coordinates = find_coordinates(nodeDict, node_id)
                            lat = coordinates['lat']
                            lon = coordinates['lon']
                            geocode += lon + ' ' + lat
                        geocode += '))'
                else:
                    geocode = 'POINT(' + lon + ' ' + lat + ')'

            if len(street) > 0 and len(housenumber) > 0:
                if len(postcode) > 0 and postcode[0].attrib['v'] not in postal_codes:
                    continue

                plz = find_plz(postcode, street[0].attrib['v'], housenumber[0].attrib['v'], geocode)

                if plz != None and plz in postal_codes:
                    writer.writerow([plz, street[0].attrib['v'], housenumber[0].attrib['v'], geocode])

        for building in unknownBuildings:
            plz = find_plz(None, building['street'], building['housenumber'], building['geocode'])

            if plz != None and plz in postal_codes:
                writer.writerow([plz, building['street'], building['housenumber'], building['geocode']])

    print('Finished.')

address_generate(['69115', '69117', '69118', '69120', '69121', '69123', '69124', '69126'])
