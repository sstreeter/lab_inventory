from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from app.auth_access_control import require_admin
from app import db
from app.models import Lab, Computer
import csv, os, json
from collections import defaultdict

admin = Blueprint('admin', __name__, url_prefix='/admin')

BACKUP_DIR = '/tmp/backups'
os.makedirs(BACKUP_DIR, exist_ok=True)

@admin.route('/labs')
@require_admin
def admin_dashboard():
    labs = Lab.query.all()
    return render_template('admin_dashboard.html', labs=labs)

@admin.route('/import', methods=['GET', 'POST'])
@require_admin
def import_csv():
    if request.method == 'POST':
        mode = request.form.get('mode')
        file = request.files.get('csv_file')

        if not file:
            flash("No file selected", 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join('/tmp', filename)
        file.save(filepath)

        conflicts = []
        imported_data = defaultdict(list)

        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [field.strip() for field in reader.fieldnames]
            for row in reader:
                lab_name = row.get("Lab", "").strip()
                identifier = ""
                if row.get("ComputerName", "").strip():
                    identifier = f"CN:{row['ComputerName'].strip()}"
                elif row.get("SerialNumber", "").strip():
                    identifier = f"SN:{row['SerialNumber'].strip()}"
                elif row.get("MAC", "").strip():
                    identifier = f"MAC:{row['MAC'].strip()}"
                if not identifier:
                    continue
                imported_data[lab_name].append({
                    'identifier': identifier,
                    'owner': row.get('Owner', '').strip(),
                    'justification': row.get('BusinessJustification', '').strip()
                })

        for lab_name, devices in imported_data.items():
            lab = Lab.query.filter_by(name=lab_name).first()
            if not lab:
                lab = Lab(name=lab_name)
                db.session.add(lab)
                db.session.commit()

            existing_computers = Computer.query.filter_by(lab_id=lab.id).all()
            existing_snapshot = [{
                'identifier': comp.computer_name or comp.serial_number or comp.mac_address,
                'owner': comp.owner,
                'justification': comp.justification
            } for comp in existing_computers]

            if mode != 'revert':
                with open(os.path.join('/tmp/backups', f"{lab.name}.json"), 'w') as bf:
                    json.dump(existing_snapshot, bf)

            if mode == 'revert':
                backup_file = os.path.join('/tmp/backups', f"{lab.name}.json")
                if os.path.exists(backup_file):
                    with open(backup_file, 'r') as bf:
                        restored = json.load(bf)
                    Computer.query.filter_by(lab_id=lab.id).delete()
                    for item in restored:
                        db.session.add(Computer(
                            computer_name=item['identifier'][3:] if item['identifier'].startswith("CN:") else None,
                            serial_number=item['identifier'][3:] if item['identifier'].startswith("SN:") else None,
                            mac_address=item['identifier'][4:] if item['identifier'].startswith("MAC:") else None,
                            owner=item['owner'],
                            justification=item['justification'],
                            lab=lab
                        ))
                    continue

            if mode == 'overwrite':
                Computer.query.filter_by(lab_id=lab.id).delete()

            for device in devices:
                identifier = device['identifier']
                existing = None
                if identifier.startswith("CN:"):
                    existing = Computer.query.filter_by(lab_id=lab.id, computer_name=identifier[3:]).first()
                elif identifier.startswith("SN:"):
                    existing = Computer.query.filter_by(lab_id=lab.id, serial_number=identifier[3:]).first()
                elif identifier.startswith("MAC:"):
                    existing = Computer.query.filter_by(lab_id=lab.id, mac_address=identifier[4:]).first()

                if existing:
                    if mode == 'retain':
                        continue
                    elif mode == 'merge':
                        changed = False
                        if device['owner'] and device['owner'] != existing.owner:
                            changed = True
                        if device['justification'] and device['justification'] != existing.justification:
                            changed = True
                        if changed:
                            conflicts.append({
                                'lab': lab.name,
                                'identifier': device['identifier'],
                                'new': device,
                                'existing': {
                                    'owner': existing.owner,
                                    'justification': existing.justification
                                }
                            })
                            existing.owner = device['owner']
                            existing.justification = device['justification']
                    elif mode == 'overwrite':
                        existing.owner = device['owner']
                        existing.justification = device['justification']
                else:
                    kwargs = {
                        'owner': device['owner'],
                        'justification': device['justification'],
                        'lab': lab
                    }
                    if identifier.startswith("CN:"):
                        kwargs['computer_name'] = identifier[3:]
                    elif identifier.startswith("SN:"):
                        kwargs['serial_number'] = identifier[3:]
                    elif identifier.startswith("MAC:"):
                        kwargs['mac_address'] = identifier[4:]
                    db.session.add(Computer(**kwargs))

        db.session.commit()
        os.remove(filepath)

        if conflicts:
            session['conflicts'] = conflicts
            return redirect(url_for('admin.resolve_conflicts'))

        flash("Import completed successfully", 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('import_csv.html')

@admin.route('/resolve-conflicts', methods=['GET', 'POST'])
@require_admin
def resolve_conflicts():
    conflicts = session.get('conflicts', [])
    if request.method == 'POST':
        for c in conflicts:
            action = request.form.get(f"resolve_{c['lab']}_{c['identifier']}")
            lab = Lab.query.filter_by(name=c['lab']).first()
            comp = Computer.query.filter_by(lab_id=lab.id, computer_name=c['identifier'][3:] if c['identifier'].startswith("CN:") else None).first()
            if not comp:
                continue
            if action == 'use_new':
                comp.owner = c['new']['owner']
                comp.justification = c['new']['justification']
        db.session.commit()
        session.pop('conflicts', None)
        flash("Conflicts resolved.", 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('conflicts.html', conflicts=conflicts)
