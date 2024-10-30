import os


class Config(object):
    SESSION_TYPE = 'filesystem'
    COMPRESS_REGISTER = os.environ.get("COMPRESS_REGISTER", "True").lower() in ["true", "1"]
    MYSQL_CONNECTION = os.environ.get("MYSQL_CONNECTION", '{ "user": "iago", "password": "I@go7881", "host": "desafio-projeto-dio-iago.mysql.database.azure.com", "database": "teste" }')
    #MYSQL_CONNECTION = os.environ.get("MYSQL_CONNECTION", '{ "user": "Iago", "password": "I@go222224", "host": "localhost", "database": "lakatos" }')