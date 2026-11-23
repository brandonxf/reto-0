from tests.conftest import registrar_y_entrar


def test_gasto_inexistente_responde_404(cliente):
    registrar_y_entrar(cliente, "usuario1", "Clave123*")
    respuesta = cliente.get("/gastos/99999/editar")
    assert respuesta.status_code == 404
