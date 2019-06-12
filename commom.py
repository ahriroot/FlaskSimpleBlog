from models import User, Category, Article
from flask import Flask, request, redirect, url_for, session, g


def all_cate():
    return Category.query.all()


def all_art():
    return Article.query.all()


def all_user():
    return User.query.all()


def account():
    id = session.get('user_id')
    if session.get('user_id'):
        leave = User.query.filter(User.id == id).first().leave
        return leave
    else:
        return 0
