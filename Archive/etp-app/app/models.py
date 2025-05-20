from . import db

class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100))
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'))
    lab = db.relationship('Lab', backref=db.backref('computers', lazy=True))

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))
    justification = db.Column(db.Text)
    computer = db.relationship('Computer', backref=db.backref('submission', uselist=False))