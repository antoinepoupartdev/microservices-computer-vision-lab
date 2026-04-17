from flask import Flask
from pathlib import Path
from routes import book_blueprint
from models import db, init_app
from flask_migrate import Migrate

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / 'database'
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / 'book.db'

app.config['SECRET_KEY'] = 'dhjkfdskjfhjk326t487236784'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH.as_posix()}"

app.register_blueprint(book_blueprint)
init_app(app)

migrate = Migrate(app, db)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)