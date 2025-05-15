from app import create_app, db
from app.models import Lab, Computer
import csv

app = create_app()

with app.app_context():
    db.create_all()
    if not Lab.query.first():
        with open('data/exceptions_sample.csv') as f:
            reader = csv.DictReader(f)
            labs = {}
            for row in reader:
                lab_name = row['Lab']
                if lab_name not in labs:
                    labs[lab_name] = Lab(name=lab_name)
                    db.session.add(labs[lab_name])
                comp = Computer(name=row['ComputerName'], owner=row['Owner'], lab=labs[lab_name])
                db.session.add(comp)
            db.session.commit()