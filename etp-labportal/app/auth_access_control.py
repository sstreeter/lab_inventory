from functools import wraps
from flask import session, redirect, url_for, flash

def require_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'admin':
            flash("Admin access required.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def restrict_lab_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'lab':
            flash("Lab user access required.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
