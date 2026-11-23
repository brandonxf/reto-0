import sqlite3

import app as app_module
from tests.conftest import registrar_y_entrar


def test_pagina_de_login_responde(cliente):
    assert cliente.get("/login").status_code == 200


def test_la_contrasena_se_guarda_con_hash(cliente):
    registrar_y_entrar(cliente, "usuario_prueba", "Clave123*")
    guardada = sqlite3.connect(app_module.DATABASE).execute(
        "SELECT password FROM usuarios WHERE username = 'usuario_prueba'"
    ).fetchone()[0]
    assert guardada != "Clave123*"
