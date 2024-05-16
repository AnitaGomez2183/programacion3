from flask import Blueprint, render_template
from sqlalchemy import text
from .models import Server, Channel
from app import db

main = Blueprint('main', __name__)

def get_servers():
    return Server.query.all()

def get_channels(server_id):
    return Channel.query.filter_by(server_id=server_id).all()

@main.route('/')
def index():
    servers = get_servers()
    return render_template('index.html', servers=servers)

@main.route('/server/<int:server_id>')
def server(server_id):
    servers = get_servers()
    channels = get_channels(server_id)
    server = Server.query.get_or_404(server_id)
    return render_template('server.html', servers=servers, channels=channels, server=server)

@main.route('/channel/<int:channel_id>')
def channel(channel_id):
    servers = get_servers()
    channel = Channel.query.get_or_404(channel_id)
    server = Server.query.get_or_404(channel.server_id)
    channels = get_channels(channel.server_id)

    query = text("""
        SELECT
            message_date,
            message_id,
            user_id,
            channel_id,
            content,
            creation_date,
            username
        FROM teamhub.view_messages_by_day
        WHERE channel_id = :channel_id
        ORDER BY message_date, creation_date
    """)
    
    result = db.session.execute(query, {"channel_id": channel_id})
    messages_by_day = result.fetchall()
    
    # Agrupar mensajes por día
    messages_grouped_by_day = {}
    for row in messages_by_day:
        message_date = row.message_date
        if message_date not in messages_grouped_by_day:
            messages_grouped_by_day[message_date] = []
        messages_grouped_by_day[message_date].append(row)

    return render_template('channel.html', servers=servers, channels=channels, server=server, channel=channel, messages_grouped_by_day=messages_grouped_by_day)
