import os

os.environ.setdefault("SECRET_KEY", "clave-solo-para-pruebas")

import pytest

import app as app_module


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "DATABASE", str(tmp_path / "prueba.db"))
    app_module.init_db()
    app_module.app.config["PROPAGATE_EXCEPTIONS"] = False
    return app_module.app.test_client()


def registrar_y_entrar(cliente, usuario, clave):
    cliente.post("/register", data={"username": usuario, "password": clave})
    cliente.post("/login", data={"username": usuario, "password": clave})
