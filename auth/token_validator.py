"""Patrón Strategy: la forma de validar un token es intercambiable.

El validador se inyecta en create_app(); ya no hay estado global mutable.
"""
from abc import ABC, abstractmethod

import config


class TokenValidator(ABC):
    @abstractmethod
    def is_valid(self, token: str) -> bool:
        ...


class StaticTokenValidator(TokenValidator):
    """Compara contra un token fijo (el que devuelve /auth)."""

    def __init__(self, expected_token: str = config.DEMO_TOKEN):
        self._expected = expected_token

    def is_valid(self, token: str) -> bool:
        return token == self._expected
