from hdbcli import dbapi
import sys
import configparser
import datetime
import random
from os import path
from pprint import pprint
from datetime import timedelta

import model_generator
import weather
import holiday
import users
import math_utils

today = datetime.date.today()
weather_year_data = [x for x in weather.get_weather_data() if x['date'].year == today.year]
if len(weather_year_data) == 0:
    print("No weather data found for the year %s"%today.year)
    sys.exit(1)
holidays = holiday.get_holiday_data()
user_data = users.generate_data()

dates = [datetime.date(today.year - 1, 1, 1) + datetime.timedelta(days=i) for i in range(365 * 2)]

insertAddressTemplate = '''
                    insert into "ADDRESSES"
                    (idUser, street, housenumber, plz, city, country, geocode)
                    values(:1, :2, :3, :4, :5, :6, {})
                '''
insertAddress = insertAddressTemplate.format(':7')
insertAddressWithPoint = insertAddressTemplate.format('ST_GeomFromWKT(:7, 4326)')
insertAddressWithPolygon = insertAddressTemplate.format("new ST_Polygon(:7, 1000004326).ST_Centroid().ST_Transform(4326)")

# Loop weather data

weather_loop_data = []

for i, date in enumerate(dates):
    data = weather_year_data[i % len(weather_year_data)].copy()
    data['date'] = date
    weather_loop_data.append(data)

def generate_orders():
    temperatures = [data['temperature'] for data in weather_loop_data]
    holiday_dates = [data['date'] for data in holidays]

    # 0 Spicy Fried Rice T▼ WT-
    # 1 Salad T▲ WT-
    # 2 Chicken T- WT-
    # 3 Beef T▼ WT Son
    # 4 Fish/Prawns T- WT Fri
    # 5 Beer T▲ WT Fri,Sam,Son
    # 6 Tea T▼ WT-

    dish_ids = range(7)
    # 50 orders for main meals, 40 orders for drinks, the daily orders maximum is 90
    weights = [10, 10, 10, 10, 10, 20, 20]

    return model_generator.generate_data(dish_ids, weights, dates, temperatures, holiday_dates)

orders = generate_orders()

def clean_up(config):
    connection = create_connection(config)
    cursor = connection.cursor()

    tables = [
        '"DATEINFO"',
        '"ORDERDISHEXTRAINGREDIENT"',
        '"ORDERLINE"',
        '"ORDERS"',
        '"INVITEDGUEST"',
        '"BOOKING"',
        '"ADDRESSES"',
        '"USER"'
    ]

    for table in tables:
        if table == '"USER"':
            query ="""delete from "USER" where "USERNAME" NOT IN ('manager', 'waiter', 'user0', 'cook', 'barkeeper', 'chief')"""
            cursor.execute(query)
        else:
            cursor.execute('delete from {}'.format(table))

    connection.commit()

def insert_users(config):
    connection = create_connection(config)
    cursor = connection.cursor()
    old_percent = -1
    isHANAExpress = config.getboolean('hana', 'express_edition', fallback=False)

    for i, row in enumerate(user_data):
        try:
            cursor.execute(
                '''
                    insert into "USER"
                    (id, modificationCounter, username, password, email, idRole)
                    values(:1, 1, :2, :3, :4, 0)
                ''',
                (
                    row['id'],
                    row['username'],
                    row['password'],
                    row['email']
                )
            )

            sql = insertAddress
            if isHANAExpress and row['geocode'] is not None:
                if row['geocode'].startswith('POLYGON'):
                    sql = insertAddressWithPolygon
                else:
                    sql = insertAddressWithPoint
            cursor.execute(
                sql,
                (
                    row['id'],
                    row['street'],
                    row['housenumber'],
                    row['plz'],
                    row['city'],
                    row['country'],
                    row['geocode']
                )
            )
        except ValueError:
            pass
        except dbapi.Error as e:
            print ("Unable to import address " + str(row['id']) + ": " + e)
            pass

        percent = round(i * 100 / len(user_data))
        if percent != old_percent:
            sys.stdout.write('\r{}% inserted...'.format(percent))
            old_percent = percent

    print()
    connection.commit()

def insert_date_info(config):
    connection = create_connection(config)
    cursor = connection.cursor()
    old_percent = -1

    for i, row in enumerate(weather_loop_data):
        try:
            designation = next((x['designation'] for x in holidays if x['date'] == row['date']), None)
            cursor.execute(
                'insert into "DATEINFO" values(:1, :2, :3)',
                (row['date'], row['temperature'], designation)
            )
        except ValueError:
            pass

        percent = round(i * 100 / len(weather_loop_data))
        if percent != old_percent:
            sys.stdout.write('\r{}% inserted...'.format(percent))
            old_percent = percent

    print()
    connection.commit()

def get_geo_weights(dish_id):
    return {
        # Weststadt, Bahnstadt, Bergheim
        '69115': (
            2 if dish_id in [0, 1, 5]
            else 4 if dish_id in [2, 4]
            else 3
        ),
        # Altstadt
        '69117': (
            1 if dish_id in [0, 1, 5]
            else 5 if dish_id in [4, 6]
            else 3
        ),
        # Ziegelhausen
        '69118': (
            1 if dish_id in [0, 1, 5]
            else 5 if dish_id in [4, 6]
            else 3
        ),
        # Neuenheim
        '69120': (
            4 if dish_id in [0, 5]
            else 5 if dish_id in [1, 6]
            else 3
        ),
        # Handschuhsheim
        '69121': (
            1 if dish_id in [4, 5]
            else 2 if dish_id == 0
            else 4 if dish_id in [3, 6]
            else 5 if dish_id in [1, 2]
            else 3
        ),
        # Wieblingen
        '69123': (
            1 if dish_id in [0, 3, 4, 5]
            else 5 if dish_id in [1, 6]
            else 3
        ),
        # Kirchheim
        '69124': (
            2 if dish_id == 5
            else 4 if dish_id == 2
            else 5 if dish_id in [3, 6]
            else 3
        ),
        # Rohrbach, Südstadt
        '69126': (
            4 if dish_id in [2, 5]
            else 2 if dish_id == 3
            else 3
        )
    }

def get_dish_users(dish_id):
    dish_users = []
    dates = []
    dish_orders = (x for x in orders if x['dish_id'] == dish_id)
    plz_list = get_geo_weights(0).keys()
    plz_users = {}

    for plz in plz_list:
        plz_users[plz] = [user for user in user_data if user['plz'] == plz]

    for order_data in dish_orders:
        weights = list(get_geo_weights(dish_id).values())
        partition = math_utils.integer_partition(order_data['orders'], weights)

        for (plz, part) in zip(plz_list, partition):
            dish_users += random.choices(plz_users[plz], k=part)
            dates += [order_data['date']] * part

    return list(zip(dates, dish_users))

def insert_orders(config):
    booking_id = 0
    order_id = 0
    order_line_id = 0

    dish_ids = set([order_data['dish_id'] for order_data in orders])

    for dish_id in dish_ids:
        connection = create_connection(config)
        cursor = connection.cursor()

        dish_users = get_dish_users(dish_id)
        old_percent = -1

        for i, (date, user) in enumerate(dish_users):
            # Insert booking

            cursor.execute(
                '''
                    insert into "BOOKING"
                    ("ID", "MODIFICATIONCOUNTER", "IDUSER", "NAME", "EMAIL", "BOOKINGDATE", "EXPIRATIONDATE", "CREATIONDATE", "BOOKINGTYPE", "IDTABLE", "IDORDER", "ASSISTANTS")
                    values(:1, 1, :2, :3, :4, :5, :5, :5, 0, 1, 0, 0)
                ''',
                (
                    booking_id,
                    user['id'],
                    user['name'],
                    user['email'],
                    datetime.datetime(date.year, date.month, date.day)
                )
            )

            # Insert order

            cursor.execute(
                '''
                    insert into "ORDERS"
                    ("ID", "MODIFICATIONCOUNTER", "IDBOOKING", "IDINVITEDGUEST", "IDHOST")
                    values(:1, 1, :2, NULL, NULL)
                ''',
                (order_id, booking_id)
            )

            # Insert order line

            cursor.execute(
                '''
                    insert into "ORDERLINE"
                    ("ID", "MODIFICATIONCOUNTER", "IDDISH", "AMOUNT", "IDORDER")
                    values(:1, 1, :2, 1, :3)
                ''',
                (order_line_id, dish_id, order_id)
            )

            booking_id += 1
            order_id += 1
            order_line_id += 1

            percent = round(i * 100 / len(dish_users))
            if percent != old_percent:
                sys.stdout.write('\rDish {}: {}% inserted...'.format(dish_id, percent))
                old_percent = percent

            connection.commit()

        print()

def create_connection(config):
    connection = dbapi.connect(
        address=config['hana']['host'],
        port=config['hana']['port'],
        user=config['hana']['user'],
        password=config['hana']['password']
    )

    return connection

def main():
    config = configparser.ConfigParser()
    config.read(path.join(path.dirname(path.dirname(__file__)), 'config.ini'))

    print('Clean up...')
    clean_up(config)

    print('Insert users...')
    insert_users(config)

    print('Insert date info...')
    insert_date_info(config)

    print('Insert orders...')
    insert_orders(config)

    print('Finished.')

if __name__ == '__main__':
    main()
