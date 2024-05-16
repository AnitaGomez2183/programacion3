from flask import Blueprint, render_template
from sqlalchemy import text
from .models import Server, Channel, User, Message
from app import db
from flask import request, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def index():
    servers = get_servers()
    return render_template('index.html', servers=servers)

def get_servers():
    query = text("SELECT * FROM view_servers")
    result = db.session.execute(query)
    servers = result.fetchall()
    return servers

@main.route('/server/<int:server_id>')
def server(server_id):
    # Obtener servidor
    server_query = text("SELECT * FROM view_servers WHERE server_id = :server_id")
    server_result = db.session.execute(server_query, {"server_id": server_id})
    server = server_result.fetchone()

    # Obtener canales del servidor
    channels_query = text("SELECT * FROM view_channels WHERE server_id = :server_id")
    channels_result = db.session.execute(channels_query, {"server_id": server_id})
    channels = channels_result.fetchall()

    # Obtener usuarios matriculados en el servidor
    users_query = text("SELECT * FROM view_users_in_server WHERE server_id = :server_id")
    users_result = db.session.execute(users_query, {"server_id": server_id})
    users = users_result.fetchall()

    servers = get_servers()
    return render_template('server.html', servers=servers, channels=channels, server=server, users=users)

@main.route('/channel/<int:channel_id>')
def channel(channel_id):
    # Obtener canal
    channel_query = text("SELECT * FROM view_channels WHERE channel_id = :channel_id")
    channel_result = db.session.execute(channel_query, {"channel_id": channel_id})
    channel = channel_result.fetchone()

    # Obtener mensajes del canal agrupados por día
    messages_query = text("""
        SELECT
            DATE(creation_date) as message_date,
            message_id,
            user_id,
            channel_id,
            content,
            creation_date,
            username
        FROM view_messages_by_day
        WHERE channel_id = :channel_id
        ORDER BY creation_date
    """)
    messages_result = db.session.execute(messages_query, {"channel_id": channel_id})
    messages_by_day = messages_result.fetchall()

    # Agrupar mensajes por día
    messages_grouped_by_day = {}
    for message in messages_by_day:
        message_date = message.message_date
        if message_date not in messages_grouped_by_day:
            messages_grouped_by_day[message_date] = []
        messages_grouped_by_day[message_date].append(message)

    servers = get_servers()
    channels = get_channels(channel.server_id)
    users = get_users(channel.server_id)
    return render_template('channel.html', servers=servers, channels=channels, channel=channel, messages_grouped_by_day=messages_grouped_by_day, users=users)

def get_channels(server_id):
    query = text("SELECT * FROM view_channels WHERE server_id = :server_id")
    result = db.session.execute(query, {"server_id": server_id})
    channels = result.fetchall()
    return channels

def get_users(server_id):
    query = text("SELECT * FROM view_users_in_server WHERE server_id = :server_id")
    result = db.session.execute(query, {"server_id": server_id})
    users = result.fetchall()
    return users

@main.route('/send_message/<int:channel_id>', methods=['POST'])
def send_message(channel_id):
    content = request.form['message']  # Asegúrate de que el nombre del campo coincida con el formulario
    user_id = 1  # Este sería el ID del usuario que envía el mensaje; en una app real, se obtendría del contexto del usuario logueado

    # Llamar al procedimiento almacenado
    query = text("CALL send_message(:p_content, :p_user_id, :p_channel_id)")
    db.session.execute(query, {'p_content': content, 'p_user_id': user_id, 'p_channel_id': channel_id})
    db.session.commit()

    return redirect(url_for('main.channel', channel_id=channel_id))
