import os


class Config:

    SECRET_KEY = '222af70ab6aa9f0f3dc81f5b35da871a'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    #SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'przykladowy0email@gmail.com'
    MAIL_PASSWORD = 'Awawaw2@'
