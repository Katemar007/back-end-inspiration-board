from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .models import board, card
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .routes.card_routes import bp as cards_bp
from .routes.board_routes import bp as boards_bp

# Import models, blueprints, and anything else needed to set up the app or database


def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Blueprints 
    app.register_blueprint(boards_bp)
    app.register_blueprint(cards_bp)
    
    frontend_url = os.environ.get('FRONTEND_URL')
    CORS(app, origins=os.environ.get(frontend_url))
    return app
