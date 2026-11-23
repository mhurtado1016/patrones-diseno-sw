"""Configuración central. Antes estaba dispersa como 'números mágicos' en cada endpoint."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "db.json"))

# Credenciales y token de demostración (fake, solo para el curso).
DEMO_USERNAME = "student"
DEMO_PASSWORD = "desingp"
DEMO_TOKEN = "abcd12345"
