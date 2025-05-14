# Flask entry point with DB setup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.inventory import inventory_bp
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/inventory_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.register_blueprint(inventory_bp, url_prefix='/api/inventory')

@app.route('/')
def index():
    return "Lab Inventory API running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)