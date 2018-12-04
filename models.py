# from sqlalchemy.sql import func
"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database. """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User table"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(
        db.Text, default="https://i.stack.imgur.com/34AD2.jpg")


class Post(db.Model):
    """Post table"""
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')


class Tag(db.Model):
    """ Tag table """
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(5), unique=True)


class PostTag(db.Model):
    """ PostTag table"""
    __tablename__ = "post_tags"
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        nullable=False,
        primary_key=True)
    tag_id = db.Column(
        db.Integer, db.ForeignKey('tags.id'), nullable=False, primary_key=True)
