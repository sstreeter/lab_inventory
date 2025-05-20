# app/auth.py

from functools import wraps
from flask import redirect, url_for, session, flash

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'admin':
            flash("Admin access required.", "danger")
            return redirect(url_for('login'))  # Change 'login' to your actual login route
        return f(*args, **kwargs)
    return decorated_function
