from app import db

class Server(db.Model):
    __tablename__ = 'view_servers'
    server_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    icon = db.Column(db.String(255))

class Channel(db.Model):
    __tablename__ = 'view_channels'
    channel_id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)

class Message(db.Model):
    __tablename__ = 'view_messages'
    message_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    channel_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    username = db.Column(db.String(50))

class User(db.Model):
    __tablename__ = 'view_users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(255))
    profile_image = db.Column(db.String(255))
    server_id = db.Column(db.Integer)

class MessageByDay(db.Model):
    __tablename__ = 'view_messages_by_day'
    message_date = db.Column(db.Date, primary_key=True)
    message_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    channel_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    username = db.Column(db.String(50))