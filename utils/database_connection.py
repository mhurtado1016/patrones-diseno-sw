"""Patrón Singleton (por ruta de archivo).

Antes cada request creaba un DatabaseConnection nuevo que releía el JSON completo,
y cada recurso mantenía una copia propia de los datos (inconsistencias entre copias).
Ahora existe UNA conexión por archivo, compartida y protegida con un lock.
"""
import json
import os
import tempfile
import threading


class DatabaseConnection:
    _instances: dict = {}
    _instances_lock = threading.Lock()

    def __new__(cls, json_file_path: str):
        path = os.path.abspath(json_file_path)
        with cls._instances_lock:
            instance = cls._instances.get(path)
            if instance is None:
                instance = super().__new__(cls)
                instance._init(path)
                cls._instances[path] = instance
            return instance

    def _init(self, path: str) -> None:
        self.json_file_path = path
        self._lock = threading.RLock()
        self._data = self._load()

    def _load(self) -> dict:
        try:
            with open(self.json_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get_collection(self, name: str) -> list:
        with self._lock:
            return list(self._data.get(name, []))

    def save_collection(self, name: str, items: list) -> None:
        with self._lock:
            new_data = {**self._data, name: list(items)}
            self._write_atomically(new_data)
            self._data = new_data  # solo se actualiza la memoria si el disco se escribió bien

    def _write_atomically(self, data: dict) -> None:
        """Escribe a un temporal y lo renombra: nunca deja el JSON a medias."""
        directory = os.path.dirname(self.json_file_path)
        fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            os.replace(tmp_path, self.json_file_path)
        except Exception:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise

    @classmethod
    def reset(cls) -> None:
        """Descarta las instancias (útil en pruebas)."""
        with cls._instances_lock:
            cls._instances.clear()
