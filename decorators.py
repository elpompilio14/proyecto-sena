from functools import wraps
from flask import session, redirect


def require_auth(f):
    @wraps(f)
    def envoltura(*args, **kwargs):
        if not session.get('usuario'):
            return redirect('/login')
        return f(*args, **kwargs)
    return envoltura


def require_admin(f):
    @wraps(f)
    def envoltura(*args, **kwargs):
        usuario = session.get('usuario')
        if not usuario or usuario.get('rol') != 'admin':
            return redirect('/login')
        return f(*args, **kwargs)
    return envoltura
