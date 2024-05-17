from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db, login_manager

# from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

auth = Blueprint("auth", __name__)


@login_manager.unauthorized_handler
def unauthorized():
    flash("Debes iniciar sesión para acceder a esta página.", "warning")
    return redirect(url_for("auth.login"))


@login_manager.user_loader
def load_user(user_id):
    stmt = text(
        "SELECT user_id, username, email FROM view_users WHERE user_id = :user_id"
    )
    result = db.session.execute(stmt, {"user_id": user_id}).fetchone()

    if result:
        return User(
            user_id=result[0],
            username=result[1],
            email=result[2],
            password=None,
        )
    return None


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Llamada al procedimiento almacenado authenticate_user
        stmt = text(
            """
            CALL authenticate_user(:p_email, :p_password, @p_user_id, @p_username);
        """
        )
        db.session.execute(stmt, {"p_email": email, "p_password": password})

        # Consulta para obtener los valores de salida
        output = db.session.execute(
            text("SELECT @p_user_id AS p_user_id, @p_username AS p_username")
        ).fetchone()
        user_id = output[0]
        username = output[1]

        if user_id and user_id > 0:
            user = User(
                user_id=user_id, username=username, email=email, password=password
            )
            login_user(user)
            return redirect(url_for("main.index"))

        flash(
            "Email o contraseña incorrectos. Por favor, inténtelo de nuevo.", "danger"
        )
        return redirect(url_for("auth.login"))
    return render_template("login.html", show_columns=False)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Llamada al procedimiento almacenado register_user
        stmt = text(
            """
            CALL register_user(:p_username, :p_email, :p_password, @p_user_id);
        """
        )
        db.session.execute(
            stmt, {"p_username": username, "p_email": email, "p_password": password}
        )

        # Consulta para obtener el valor de salida
        output = db.session.execute(text("SELECT @p_user_id")).fetchone()
        user_id = output[0]  # Acceder por índice

        if user_id and user_id > 0:
            flash("Cuenta creada con éxito. Por favor, inicie sesión.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Error al crear la cuenta. Por favor, inténtelo de nuevo.", "danger")
            return redirect(url_for("auth.register"))
    return render_template("register.html", show_columns=False)
