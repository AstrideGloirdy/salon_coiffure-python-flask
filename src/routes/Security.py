from functools import wraps
from flask import redirect, url_for, flash,abort,render_template
from flask_login import current_user



def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'admin':
            abort(403)  # Accès interdit si l'utilisateur n'est pas administrateur
        return func(*args, **kwargs)
    return decorated_view

def cassier_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'gestionnaire':
            abort(403)  # Accès interdit si l'utilisateur n'est pas gestionnaire
        return func(*args, **kwargs)
    return decorated_view

def gestionnaire_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'caissier':
            abort(403)  # Accès interdit si l'utilisateur n'est pas caissier
        return func(*args, **kwargs)
    return decorated_view



