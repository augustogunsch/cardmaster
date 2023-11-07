import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .extensions import db
from .routes import user_bp, deck_bp, auth_bp, card_bp

load_dotenv()

uri = os.getenv('DATABASE_URL')

if uri.startswith('postgres://'): # pragma: no cover
    uri = uri.replace('postgres://', 'postgresql://', 1)

os.environ['FLASK_SQLALCHEMY_DATABASE_URI'] = uri

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    db.init_app(app)

    migrate = Migrate(app, db)

    CORS(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(deck_bp)
    app.register_blueprint(card_bp)

    return app
