from flask import Flask
from flask_session import Session
from flask_compress import Compress
from blueprints.page import page
from libs.sql import configMySql
from config import *


app = Flask(__name__, static_url_path='', static_folder='static')
app.config.from_object(Config)

configMySql(app)

app.register_blueprint(page)

Session(app)
Compress(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)