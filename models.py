from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    f_name = db.Column(db.String(20),
                    nullable=False,
                    unique=False)
    l_name = db.Column(db.String(20),
                    nullable=False,
                    unique=False)
    img_url = db.Column(db.String,
                    nullable=False,
                    default='http://www.newdesignfile.com/postpic/2009/09/generic-user-icon-windows_354183.png')


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                    nullable=False,
                    unique=False)
    content = db.Column(db.String(240),
                    nullable=False,
                    unique=False)
    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'))
    post_tags = db.relationship('Tag',
                    secondary='post_tags',
                    backref='post')


class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
                    "posts.id"),
                    primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
                    "tags.id"),
                    primary_key=True)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(50),
                    nullable=False,
                    unique=True)
    post_tags = db.relationship('Post',
                    secondary='post_tags',
                    backref='tag')


