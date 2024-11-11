import os

class Config(object):
    # Configurações de sessão e compressão
    SESSION_TYPE = 'filesystem'
    COMPRESS_REGISTER = os.environ.get("COMPRESS_REGISTER", "True").lower() in ["true", "1"]

    # Configurações de banco de dados
    # MYSQL_CONNECTION = os.environ.get("MYSQL_CONNECTION", '{ "user": "Iago", "password": "I@go222224", "host": "localhost", "database": "teste", "auth_plugin":"mysql_native_password"}')
    MYSQL_CONNECTION = os.environ.get("MYSQL_CONNECTION", '{ "user": "root", "password": "I@go222224", "host": "localhost", "database": "teste", "auth_plugin":"mysql_native_password"}')

    # Configurações de e-mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'iago2005andrade@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'amaj qjss ortx sana')
    MAIL_DEFAULT_SENDER = ('Iago', 'iago2005andrade@gmail.com')
    OPENAI_API_KEY = os.environ.get("OPENAI_KEY")