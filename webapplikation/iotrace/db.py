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


def get_user(userID):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM user WHERE userID = ' + str(userID) + ';')
        user = cursor.fetchall()
        if result > 0:
            user_list = jsonify(user)
        else:
            user_list = 'No user with', str(userID), 'in DB.'
        return user_list

def get_device():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM device;')
        device = cursor.fetchall()
        if result > 0:
            device_list = jsonify(device)
        else:
            device_list = 'No device in DB'
    conn.close()
    return device_list

def get_device_by_userID(userID):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM device WHERE userID ='+str(userID)+';')
        device = cursor.fetchall()
        if result > 0:
            device_list = jsonify(device)
        else:
            device_list = 'No device in DB'
    conn.close()
    return device_list
