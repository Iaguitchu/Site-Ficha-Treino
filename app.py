from flask import Flask
from flask_session import Session
from flask_compress import Compress
from flask_mail import Mail
from blueprints.page import page
from libs.sql import configMySql
from config import Config

app = Flask(__name__, static_url_path='', static_folder='static')
app.config.from_object(Config)

configMySql(app)

# Inicialize o Flask-Mail e armazene em uma variável
mail = Mail(app)

# Registre o blueprint e passe o objeto `mail`
app.register_blueprint(page)

Session(app)
Compress(app)

# Disponibilize `mail` globalmente para que `page.py` possa usá-lo
app.extensions['mail'] = mail

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
