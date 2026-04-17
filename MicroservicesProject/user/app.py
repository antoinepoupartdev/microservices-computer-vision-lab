from flask import Flask, g, request
from pathlib import Path

from flask.sessions import SecureCookieSessionInterface
import models
from routes import user_blueprint
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / 'database'
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / 'users.db'

app.config['SECRET_KEY'] = 'gfdV435GBFD'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH.as_posix()}"
models.init_app(app)
app.register_blueprint(user_blueprint)
login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app, models.db)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None

class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_request'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)