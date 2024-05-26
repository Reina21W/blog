from exts import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlite3


DATABASE = 'copy.db'

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now())


class PostModel(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="posts")


class CommentModel(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    post = db.relationship(PostModel, backref=db.backref("comments", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="comments")

