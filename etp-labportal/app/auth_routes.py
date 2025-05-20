# app/auth_routes.py or wherever your auth routes are

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        session['user_role'] = user.role
        flash('Logged in successfully!', 'success')

        # Redirect based on role
        if user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('lab.lab_dashboard'))  # Or wherever lab users go

    return render_template('login.html')
