import os
import json


#For windows
class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')
	MAIL_SERVER = "smtp.googlemail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	XTEL_TOKEN = os.environ.get('XTEL_TOKEN')
	MQTT_BROKER = os.environ.get('MQTT_BROKER')
	MQTT_USER = os.environ.get('MQTT_USER')
	MQTT_PASS = os.environ.get('MQTT_PASS')
"""
# For Ubuntu
class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY')
	MAIL_SERVER = "smtp.googlemail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	XTEL_TOKEN = os.environ.get('XTEL_TOKEN')
	MQTT_BROKER = os.environ.get('MQTT_BROKER')
	MQTT_USER = os.environ.get('MQTT_USER')
	MQTT_PASS = os.environ.get('MQTT_PASS')
"""