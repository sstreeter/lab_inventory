from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

from app.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'  # Replace this with an environment variable in production
    app.config.from_object(Config)
    app.debug = True  # Remove this or configure via environment in production

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.auth_routes import auth
    from app.admin_routes import admin
    from app.lab_routes import lab
    from app.main_routes import main

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(lab)
    app.register_blueprint(main)

    return app
