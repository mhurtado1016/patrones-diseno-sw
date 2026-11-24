"""Patrón Decorator: añade autenticación a un método sin modificarlo."""
from functools import wraps

from flask import current_app, request


def require_auth(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Unauthorized access token not found"}, 401
        validator = current_app.extensions["token_validator"]
        if not validator.is_valid(token):
            return {"message": "Unauthorized invalid token"}, 401
        return method(*args, **kwargs)

    return wrapper
