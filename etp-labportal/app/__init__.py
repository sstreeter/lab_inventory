from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.auth_routes import auth

app.register_blueprint(auth)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'  # Replace securely in production
    app.config.from_object(Config)
    app.debug = True  # <-- add this line

    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints — import inside create_app to avoid circular import
    from .admin_routes import admin
    from .lab_routes import lab
    from .main_routes import main

    app.register_blueprint(admin)
    app.register_blueprint(lab)
    app.register_blueprint(main)

    return app


