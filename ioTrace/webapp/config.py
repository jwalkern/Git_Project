import os

class Config:
   SECRET_KEY = 'd70f607b41a89d8c815357cb3dcfc614'
   SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
   #SECRET_KEY = os.environ.get('SECRET_KEY')
   #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')     
   MAIL_SERVER = 'smtp.googlemail.com'
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME = os.environ.get('G_MAIL')
   MAIL_PASSWORD = os.environ.get('G_PASS')
