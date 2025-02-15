from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager, whooshee

import flask_sqlalchemy

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))
    avatar_url = db.Column(db.String(1024))

    picks = db.relationship('Pick', backref='author', lazy='dynamic')
    casts_hosting = db.relationship('Cast', backref='host', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @property
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'avatar_url': self.avatar_url,
        }

    @property
    def to_json_picks(self):
        return [ pick.to_json for pick in self.picks ]

class Cast(db.Model):
    __tablename__ = 'casts'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(80))
    date = db.Column(db.String(80))
    cast_number = db.Column(db.Integer, unique=True)
    description = db.Column(db.Text)
    picture_url = db.Column(db.String(1024))

    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    picks = db.relationship('Pick', backref='cast', lazy='dynamic')

    @property
    def to_json(self):
        return {
            'id': self.id,
            'time': self.time,
            'date': self.date,
            'cast_number': self.cast_number,
            'description': self.description,
            'picture_url': self.picture_url
        }
    @property
    def to_json_picks(self):
        return [ pick.to_json for pick in self.picks ]

@whooshee.register_model('artist', 'song', 'album', 'description')
class Pick(db.Model):
    __tablename__ = 'picks'
    id = db.Column(db.Integer, primary_key=True)
    dj_list_position = db.Column(db.Integer)
    played = db.Column(db.Boolean)
    artist = db.Column(db.String(255), index=True)
    album = db.Column(db.String(255), index=True)
    song = db.Column(db.String(255), index=True)
    description = db.Column(db.Text)
    picture_url = db.Column(db.String(1024))
    links = db.Column(db.Text)
    last_edited = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cast_id = db.Column(db.Integer, db.ForeignKey('casts.id'))

    @property
    def to_json(self):
        return {
            'id': self.id,
            'artist': self.artist,
            'album': self.album,
            'song': self.song,
            'description': self.description,
            'picture_url': self.picture_url,
            'links': self.links,
            'last_edited': self.last_edited,
            'date_added': self.date_added,
            'author_id': self.user_id,
            'username': self.author.username,
            'cast_id': self.cast_id,
            'dj_list_position': self.dj_list_position,
            'played': self.played
        }

class Link(db.Model):
    __bind_key__ = 'links'
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    nickname = db.Column(db.String)
    last_sent = db.Column(db.DateTime)

    @property
    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'nickname': self.nickname,
            'last_sent': self.last_sent
        }

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
