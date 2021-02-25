import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn


def get_device():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM entries;')
        devices = cursor.fetchall()
        if result > 0:
            device_list = jsonify(devices)
        else:
            device_list = 'No device in DB'
    conn.close()
    return device_list

def add_device(item):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO entries (deviceName, pos, lte_rssi, volt, temp, hpa, humid) VALUES (%s, %s, %s, %s, %s, %s, %s, )',
                       (item['deviceName'], item['pos'], item['lte_rssi'], item['volt'], item['temp'], item['hpa'], item['humid']))
    conn.commit()
    conn.close()
