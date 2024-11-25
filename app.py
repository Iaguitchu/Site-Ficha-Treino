from flask import Flask
from flask_session import Session
from flask_compress import Compress
from blueprints.page import page
from libs.sql import configMySql
from config import *
from flask_mail import Mail, Message
import openai

app = Flask(__name__, static_url_path='', static_folder='static')
app.config.from_object(Config)
#openai.api_key = os.environ.get("OPENAI_KEY")

app.config['OPENAI_KEY'] = os.environ.get("OPENAI_KEY")

openai.api_key = app.config['OPENAI_KEY']

configMySql(app)
app.register_blueprint(page)

mail = Mail(app)
Session(app)
Compress(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)