from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from flask_login import login_required, current_user
from app import db
import json

main = Blueprint("main", __name__)


@main.route("/")
def index():
    servers = get_servers()
    return render_template("index.html", servers=servers, show_columns=True)


@main.route("/server/<int:server_id>")
def server(server_id):
    server = get_server(server_id)
    channels = get_channels(server_id)
    users = get_users(server_id)
    servers = get_servers()
    return render_template(
        "server.html",
        servers=servers,
        channels=channels,
        server=server,
        users=users,
        show_columns=True,
    )


@main.route("/channel/<int:channel_id>")
def channel(channel_id):
    channel = get_channel(channel_id)
    messages_grouped_by_day = get_messages_grouped_by_day(channel_id)
    servers = get_servers()
    channels = get_channels(channel.server_id)
    users = get_users(channel.server_id)
    return render_template(
        "channel.html",
        servers=servers,
        channels=channels,
        channel=channel,
        messages_grouped_by_day=messages_grouped_by_day,
        users=users,
        show_columns=True,
    )


@main.route("/send_message/<int:channel_id>", methods=["POST"])
@login_required
def send_message(channel_id):
    content = request.form["message"]
    user_id = current_user.get_id()  # Obtener el ID del usuario logueado
    send_message_to_channel(content, user_id, channel_id)
    return redirect(url_for("main.channel", channel_id=channel_id))


@main.route("/create_poll/<int:channel_id>", methods=["POST"])
@login_required
def create_poll(channel_id):
    question = request.form.get("question")
    options = request.form.getlist("options")
    event_date = request.form.get("event_date")

    if not question or not options or not event_date:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for("main.channel", channel_id=channel_id))

    # Convertimos las opciones en un array JSON
    options_json = json.dumps(options)

    create_poll_in_channel(channel_id, question, options_json, event_date)
    return redirect(url_for("main.channel", channel_id=channel_id))


def get_servers():
    query = text("SELECT * FROM view_servers")
    result = db.session.execute(query)
    return result.fetchall()


def get_server(server_id):
    query = text("SELECT * FROM view_servers WHERE server_id = :server_id")
    result = db.session.execute(query, {"server_id": server_id})
    return result.fetchone()


def get_channels(server_id):
    query = text("SELECT * FROM view_channels WHERE server_id = :server_id")
    result = db.session.execute(query, {"server_id": server_id})
    return result.fetchall()


def get_users(server_id):
    query = text("SELECT * FROM view_users_in_server WHERE server_id = :server_id")
    result = db.session.execute(query, {"server_id": server_id})
    return result.fetchall()


def get_channel(channel_id):
    query = text("SELECT * FROM view_channels WHERE channel_id = :channel_id")
    result = db.session.execute(query, {"channel_id": channel_id})
    return result.fetchone()


def get_messages_grouped_by_day(channel_id):
    messages_query = text(
        "SELECT * FROM view_messages_by_day WHERE channel_id = :channel_id"
    )
    messages_result = db.session.execute(messages_query, {"channel_id": channel_id})
    messages_by_day = messages_result.fetchall()

    messages_grouped_by_day = {}
    for message in messages_by_day:
        message_date = message.message_date
        if message_date not in messages_grouped_by_day:
            messages_grouped_by_day[message_date] = []
        messages_grouped_by_day[message_date].append(message)

    return messages_grouped_by_day


def send_message_to_channel(content, user_id, channel_id):
    query = text("CALL send_message(:p_content, :p_user_id, :p_channel_id)")
    db.session.execute(
        query, {"p_content": content, "p_user_id": user_id, "p_channel_id": channel_id}
    )
    db.session.commit()


def create_poll_in_channel(channel_id, question, options, event_date):
    query = text(
        "CALL create_poll(:p_channel_id, :p_question, :p_options, :p_event_date)"
    )
    db.session.execute(
        query,
        {
            "p_channel_id": channel_id,
            "p_question": question,
            "p_options": options,
            "p_event_date": event_date,
        },
    )
    db.session.commit()
