from tests.conftest import registrar_y_entrar


def test_gasto_inexistente_responde_404(cliente):
    registrar_y_entrar(cliente, "usuario1", "Clave123*")
    respuesta = cliente.get("/gastos/99999/editar")
    assert respuesta.status_code == 404


def test_un_usuario_no_puede_ver_ni_modificar_el_gasto_de_otro(cliente):
    import sqlite3

    import app as app_module

    registrar_y_entrar(cliente, "usuario1", "Clave123*")
    cliente.post(
        "/gastos/nuevo",
        data={"descripcion": "Almuerzo", "monto": "18500", "categoria": "Otros", "fecha": "2026-11-20"},
    )
    cliente.get("/logout")
    registrar_y_entrar(cliente, "usuario2", "Clave456*")

    assert cliente.get("/gastos/1/editar").status_code in (403, 404)
    cambio = cliente.post(
        "/gastos/1/editar",
        data={"descripcion": "hackeado", "monto": "1", "categoria": "Otros", "fecha": "2026-11-20"},
    )
    assert cambio.status_code in (403, 404)
    borrado = cliente.post("/gastos/1/eliminar")
    assert borrado.status_code in (403, 404)

    descripcion = sqlite3.connect(app_module.DATABASE).execute(
        "SELECT descripcion FROM gastos WHERE id = 1"
    ).fetchone()
    assert descripcion == ("Almuerzo",)
