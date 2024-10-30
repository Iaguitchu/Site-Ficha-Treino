from flask import Flask
from flask_session import Session
from flask_compress import Compress
from blueprints.page import page

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['SESSION_TYPE'] = 'filesystem'  # Exemplo de configuração de sessão

app.register_blueprint(page)

Session(app)
Compress(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
