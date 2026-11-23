import os
import sqlite3
from datetime import date

from dotenv import load_dotenv
from flask import Flask, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
DATABASE = "gastos.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL,
            categoria TEXT NOT NULL,
            fecha TEXT NOT NULL
        );
        """
    )
    db.commit()
    db.close()


def login_required(vista):
    def envoltura(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return vista(*args, **kwargs)

    envoltura.__name__ = vista.__name__
    return envoltura


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        try:
            db.execute(
                "INSERT INTO usuarios (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="El usuario ya existe")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        usuario = db.execute(
            "SELECT * FROM usuarios WHERE username = ?", (request.form["username"],)
        ).fetchone()
        if usuario and check_password_hash(usuario["password"], request.form["password"]):
            session["user_id"] = usuario["id"]
            session["username"] = usuario["username"]
            return redirect(url_for("index"))
        return render_template("login.html", error="Credenciales incorrectas")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    db = get_db()
    gastos = db.execute(
        "SELECT * FROM gastos WHERE user_id = ? ORDER BY fecha DESC", (session["user_id"],)
    ).fetchall()
    resumen = db.execute(
        "SELECT substr(fecha, 1, 7) AS mes, categoria, SUM(monto) AS total "
        "FROM gastos WHERE user_id = ? GROUP BY mes, categoria ORDER BY mes DESC, categoria",
        (session["user_id"],),
    ).fetchall()
    return render_template("index.html", gastos=gastos, resumen=resumen, hoy=date.today().isoformat())


@app.route("/gastos/nuevo", methods=["POST"])
@login_required
def nuevo():
    db = get_db()
    db.execute(
        "INSERT INTO gastos (user_id, descripcion, monto, categoria, fecha) VALUES (?, ?, ?, ?, ?)",
        (
            session["user_id"],
            request.form["descripcion"],
            float(request.form["monto"]),
            request.form["categoria"],
            request.form["fecha"],
        ),
    )
    db.commit()
    return redirect(url_for("index"))


@app.route("/gastos/<int:gasto_id>/editar", methods=["GET", "POST"])
@login_required
def editar(gasto_id):
    db = get_db()
    if request.method == "POST":
        db.execute(
            "UPDATE gastos SET descripcion = ?, monto = ?, categoria = ?, fecha = ? WHERE id = ?",
            (
                request.form["descripcion"],
                float(request.form["monto"]),
                request.form["categoria"],
                request.form["fecha"],
                gasto_id,
            ),
        )
        db.commit()
        return redirect(url_for("index"))
    gasto = db.execute("SELECT * FROM gastos WHERE id = ?", (gasto_id,)).fetchone()
    return render_template("editar.html", gasto=gasto)


@app.route("/gastos/<int:gasto_id>/eliminar", methods=["POST"])
@login_required
def eliminar(gasto_id):
    db = get_db()
    db.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
