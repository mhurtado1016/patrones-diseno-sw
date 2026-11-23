"""Patrón Decorator: añade autenticación a un método sin modificarlo."""
from functools import wraps

from flask import request

from auth.token_validator import get_validator


def require_auth(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Unauthorized access token not found"}, 401
        if not get_validator().is_valid(token):
            return {"message": "Unauthorized invalid token"}, 401
        return method(*args, **kwargs)

    return wrapper
