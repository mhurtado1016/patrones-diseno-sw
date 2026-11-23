"""Patrón Strategy: la forma de validar un token es intercambiable."""
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


# Estrategia activa. Para usar JWT, basta con asignar otra implementación.
_validator: TokenValidator = StaticTokenValidator()


def get_validator() -> TokenValidator:
    return _validator


def set_validator(validator: TokenValidator) -> None:
    global _validator
    _validator = validator
