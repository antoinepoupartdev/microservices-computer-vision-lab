from flask import Flask
from flask_migrate import Migrate

import models
from routes import order_blueprint
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / 'database'
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / 'orders.db'

app.config['SECRET_KEY'] = 'gfdV435GBFD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH.as_posix()}"

models.init_app(app)
app.register_blueprint(order_blueprint)
migrate = Migrate(app, models.db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)