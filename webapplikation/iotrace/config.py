import os
import json

with open('config.json') as config_file:
	config = json.load(config_file)

class Config:
	SECRET_KEY = config.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
	GOOGLEMAPS_KEY = config.get('GOOGLEMAPS_KEY')
	MAIL_SERVER = "smtp.googlemail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = config.get('MAIL_USERNAME')
	MAIL_PASSWORD = config.get('MAIL_PASSWORD')
	XTEL_TOKEN = config.get('XTEL_TOKEN')

