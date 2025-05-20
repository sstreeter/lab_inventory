from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Lab, Computer, Submission

main = Blueprint('main', __name__)

@main.route('/')
def index():
    labs = Lab.query.all()
    return render_template('index.html', labs=labs)

@main.route('/lab/<int:lab_id>', methods=['GET', 'POST'])
def lab_view(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    if request.method == 'POST':
        for comp in lab.computers:
            just = request.form.get(f'justification_{comp.id}')
            if comp.submission:
                comp.submission.justification = just
            else:
                db.session.add(Submission(computer_id=comp.id, justification=just))
        db.session.commit()
        return redirect(url_for('main.lab_view', lab_id=lab_id))
    return render_template('lab_view.html', lab=lab)

@main.route('/admin')
def admin():
    submissions = Submission.query.all()
    return render_template('admin.html', submissions=submissions)