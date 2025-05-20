
from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # You should hash this!
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'lab'
    
class Lab(db.Model):
    __tablename__ = 'lab'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    computers = db.relationship('Computer', back_populates='lab', cascade='all, delete-orphan')

class Computer(db.Model):
    __tablename__ = 'computer'  # Optional: explicitly name the table

    id = db.Column(db.Integer, primary_key=True)
    computer_name = db.Column(db.String(120))         # from 'ComputerName'
    serial_number = db.Column(db.String(120))         # from 'SerialNumber'
    mac_address = db.Column(db.String(120))           # from 'MAC'
    owner = db.Column(db.String(120))                 # from 'Owner'
    justification = db.Column(db.Text)                # from 'BusinessJustification'
    
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)  # FK to Lab table
    lab = db.relationship('Lab', back_populates='computers')  # Two-way relationship
