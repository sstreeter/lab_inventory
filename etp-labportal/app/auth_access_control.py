from functools import wraps
from flask import session, redirect, url_for, flash

def require_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session:
            flash('Login required.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    @require_logged_in
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def require_lab_user(f):
    @wraps(f)
    @require_logged_in
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'lab':
            flash('Lab user access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
