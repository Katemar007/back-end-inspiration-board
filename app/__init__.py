from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .models import board, card
import os, re
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .routes.card_routes import bp as cards_bp
from .routes.board_routes import bp as boards_bp

# Import models, blueprints, and anything else needed to set up the app or database


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['CORS_HEADERS'] = 'Content-Type'

    frontend_url = os.environ.get('FRONTEND_URI')
    allowed_origins = [re.compile(r"^http://localhost:\d+/front-end-inspiration-board(/.*)?$")] #local_url

    if frontend_url:
        allowed_origins.append(frontend_url)
        CORS(
        app, 
        origins=allowed_origins,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
        print(f"CORS allowed for: {allowed_origins}")
    else:
        CORS(app)
        print("FRONTEND_URI not set. Allowing all origins.")
        

    if config:
        app.config.update(config)

    # Initialize app with SQLAlchemy db and Migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Blueprints 
    app.register_blueprint(boards_bp)
    app.register_blueprint(cards_bp)
    
    # technical route to avoid an error at deploy
    @app.route("/")
    def index():
        return {"message": "Welcome to the Inspiration Board API!"}, 200

    # frontend_url = os.environ.get('FRONTEND_URI')
    # if frontend_url:
    #     CORS(app, origins=[frontend_url])
    #     print(f"CORS allowed for: {frontend_url}")
    # else:
    #     CORS(app)
    #     print("FRONTEND_URI not set. Allowing all origins.")

    return app
