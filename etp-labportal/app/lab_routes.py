from app.auth_access_control import require_logged_in
from app.auth_access_control import restrict_lab_access
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Lab, Computer

lab = Blueprint('lab', __name__, url_prefix='/lab')

@lab.route('/')
def lab_dashboard():
    lab_name = session.get('lab')
    if not lab_name:
        flash("Lab not set in session.", "danger")
        return redirect(url_for('main.index'))
    
    lab = Lab.query.filter_by(name=lab_name).first()
    if not lab:
        flash("Lab not found.", "danger")
        return redirect(url_for('main.index'))

    return render_template('lab_dashboard.html', lab=lab)

@lab.route('/edit/<int:computer_id>', methods=['GET', 'POST'])
def edit_computer(computer_id):
    comp = Computer.query.get_or_404(computer_id)
    if request.method == 'POST':
        comp.owner = request.form.get('owner', comp.owner)
        comp.justification = request.form.get('justification', comp.justification)
        db.session.commit()
        flash("Computer updated.", "success")
        return redirect(url_for('lab.lab_dashboard'))
    return render_template('edit_computer.html', computer=comp)
