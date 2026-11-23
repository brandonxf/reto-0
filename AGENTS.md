# AGENTS.md

## Proyecto
Aplicación web de control de gastos personales. Cada usuario se registra,
inicia sesión, registra gastos por categoría y ve un resumen mensual.

## Stack
- Python 3.14 con Flask 3.1
- Base de datos SQLite (gastos.db, se crea al ejecutar)
- Plantillas Jinja2 y python-dotenv para leer el archivo .env

## Comandos
- Instalar: `python -m venv .venv`, activar y `pip install -r requirements.txt`
- Configurar: `cp .env.example .env` y escribir un SECRET_KEY propio
- Ejecutar: `python app.py` (http://127.0.0.1:5000)
- Pruebas: `python -m pytest -v`
- Estilo: `ruff check .`

## Estructura
- app.py: rutas, autenticación y acceso a datos (todo en un archivo)
- templates/: base, login, register, index y editar (HTML con Jinja2)
- requirements.txt: dependencias
- .env.example: nombres de las variables de entorno, sin valores reales
- gastos.db: base de datos de desarrollo (no se versiona)

## Qué no hacer
- No modificar las pruebas para que pasen: se corrige el código.
- No escribir claves en el código: se leen con os.environ desde .env.
- No instalar dependencias sin explicar para qué sirven.
- No hacer commit ni push.

## Lecciones aprendidas
