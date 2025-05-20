from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///etp.db'
    app.config['SECRET_KEY'] = 'supersecretkey'

    db.init_app(app)

    from .models import Lab, Computer
    from .routes import main
    app.register_blueprint(main)

    # Initialize DB at startup manually
    with app.app_context():
        initialize_database()

    return app

def initialize_database():
    from .models import Lab, Computer
    db.create_all()
    if not Lab.query.first():
        try:
            with open('data/exceptions_sample.csv') as f:
                reader = csv.DictReader(f)
                labs = {}
                for row in reader:
                    lab_name = row['Lab']
                    if lab_name not in labs:
                        labs[lab_name] = Lab(name=lab_name)
                        db.session.add(labs[lab_name])
                    comp = Computer(
                        name=row['ComputerName'],
                        owner=row['Owner'],
                        lab=labs[lab_name]
                    )
                    db.session.add(comp)
                db.session.commit()
        except FileNotFoundError:
            print("⚠️  'data/exceptions_sample.csv' not found. Skipping DB initialization.")
