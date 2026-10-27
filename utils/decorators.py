from functools import wraps
from flask import flash, redirect, url_for, render_template
from flask_login import current_user

def roles_required(*roles):
    """
    Decorator for verifying that current logged-in user possesses one of the allowed roles.
    Backend authoritative role-based access control (RBAC).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('auth.login'))
            
            user_role = getattr(current_user, 'role', '').lower()
            allowed_roles = [r.lower() for r in roles]
            
            if user_role not in allowed_roles:
                flash(f"Access denied. Required role: {', '.join(roles).upper()}.", "danger")
                return render_template('errors/403.html'), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Convenience decorator for Admin-only routes."""
    return roles_required('admin')(f)

def manager_or_admin_required(f):
    """Convenience decorator for Manager and Admin routes."""
    return roles_required('admin', 'manager')(f)
