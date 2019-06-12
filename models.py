from datetime import datetime

from exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    leave = db.Column(db.Integer, nullable=False, default=0)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cate_name = db.Column(db.String(20), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False, default=0)
    leave = db.Column(db.Integer, nullable=False, default=0)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cate_id = db.Column(db.Integer, nullable=False, default=0)
    art_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    describe = db.Column(db.Text, nullable=True)
    author = db.Column(db.Integer, nullable=True)
    time = db.Column(db.DateTime, default=datetime.now)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=True)
    user = db.Column(db.Integer, nullable=True, default=0)
    time = db.Column(db.DateTime, default=datetime.now)
