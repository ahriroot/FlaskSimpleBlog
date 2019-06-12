import os
import random
import time
from datetime import datetime

import flask
from flask import Flask, request, redirect, url_for, session, g
from flask import render_template
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from commom import all_cate, all_art, all_user, account
from models import User, Category, Article, Comment
from exts import db
import config
import platform

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


def time_reverse(time):
    if isinstance(time, datetime):
        now = datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return '刚刚'
        elif timestamp >= 60 and timestamp <= 60 * 60:
            minutes = timestamp / 60
            return '%s 分钟前' % int(minutes)
        elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
            hours = timestamp / (60 * 60)
            return '%s小时前' % int(hours)
        elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
            days = timestamp / (60 * 60 * 24)
            return '%s天前' % int(days)
        else:
            return time.strftime('%Y/%m/%d/ %H:%M')


app.add_template_filter(time_reverse, 'time')


@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    articles = Article.query.order_by(db.desc(Article.id)).all()
    # categories = Category.query.filter(Category.leave > 9).order_by(db.desc(Category.id)).all()
    categories = Category.query.filter(Category.leave > 9).all()
    for cate in categories:
        id = cate.id
    return render_template('index.html', articles=articles, categories=categories, id=id)


@app.route('/art_by_cate/', methods=['GET', 'POST'])
def art_by_cate():
    id = request.form.get('id')
    cate = Category.query.filter(Category.id == id).first()
    users = all_user()
    articles = Article.query.filter(Article.cate_id == id).all()
    return render_template('art_by_cate.html', articles=articles, users=users, cate=cate)


@app.route('/search/', methods=['GET'])
def search():
    search = request.args.get('search')
    articles = Article.query.filter(or_(Article.describe.ilike('%'+search+'%'), Article.art_name.ilike('%'+search+'%')))
    return render_template('search.html', articles=articles)


@app.route('/info/', methods=['GET', 'POST'])
def info():
    if request.method == 'GET':
        id = request.args.get('id')
        cate_id = Article.query.filter(Article.id == id).first().cate_id
        articles = Article.query.filter(Article.cate_id == cate_id).all()
        return render_template('info.html', id=id, articles=articles)
    else:
        id = request.form.get('id')
        article = Article.query.filter(Article.id == id).first()
        username = User.query.filter(User.id == article.author).first().username
        return render_template('art.html', article=article, username=username)


@app.route('/comment/', methods=['GET', 'POST'])
def comment():
    if request.method == 'GET':
        id = request.args.get('id')
        users = all_user()
        comments = Comment.query.filter(Comment.art_id == id).all()
        return render_template('comment.html', comments=comments, users=users)
    else:
        if account() < 0:
            id = request.form.get('id')
            content = request.form.get('content')
            comment = Comment(art_id=id, content=content, user=session.get('user_id'))
            db.session.add(comment)
            db.session.commit()
            return 'ok'
        else:
            return 'error'


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if account() < 0:
        return render_template('admin.html')
    else:
        # return render_template('admin.html')
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # session.permanent = True  # 保留31天
            return redirect(url_for('index'))
        else:
            return 'error'


@app.route('/logout/', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # user = User.query.filter(User.telephone == telephone).first()
        if password1 != password2:
            return 'error'
        else:
            user = User(username=username, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/sys_info/', methods=['GET', 'POST'])
def sys_info():
    if account() < 0:
        uname = platform.uname()
        info = flask.__version__
        return render_template('admin/sys_info.html', uname=uname, info=info)
    else:
        return redirect(url_for('login'))


@app.route('/category/', methods=['GET', 'POST'])
def category():
    if account() < 0:
        data = []
        par = []
        ch = []
        res = all_cate()
        for r in res:
            if r.parent_id == 0:
                par.append(r)
                for x in res:
                    if x.parent_id == r.id:
                        ch.append(x)
                par.append(ch)
                ch = []
            if par:
                data.append(par)
                par = []
        return render_template('admin/category.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/add_cate/', methods=['POST'])
def add_cate():
    if account() < 0:
        name = request.form.get('name')
        pid = request.form.get('pid')
        leave = request.form.get('leave')
        category = Category(cate_name=name, parent_id=pid, leave=leave)
        db.session.add(category)
        db.session.commit()
        return 'ok'
    else:
        return redirect(url_for('login'))


@app.route('/del_cate/', methods=['POST'])
def del_cate():
    if account() < 0:
        id = request.form.get('id')
        category = Category.query.filter(Category.id == id).first()
        if category:
            db.session.delete(category)
            db.session.commit()
            return 'ok'
        else:
            return 'no'
    else:
        return redirect(url_for('login'))


@app.route('/ch_cate/', methods=['POST'])
def ch_cate():
    if account() < 0:
        id = request.form.get('id')
        name = request.form.get('name')
        leave = request.form.get('leave')
        category = Category.query.filter(Category.id == id).first()
        if category:
            category.cate_name = name
            category.leave = leave
            db.session.commit()
            return 'ok'
        else:
            return 'no'
    else:
        return redirect(url_for('login'))


@app.route('/article/', methods=['GET', 'POST'])
def article():
    if account() < 0:
        categories = all_cate()
        articles = all_art()
        users = all_user()
        for art in articles:
            for cate in categories:
                if art.cate_id == cate.id:
                    art.cate_name = cate.cate_name
        return render_template('admin/article.html', articles=articles, users=users)
    else:
        return redirect(url_for('login'))


@app.route('/add_art/', methods=['GET', 'POST'])
def add_art():
    if account() < 0:
        if request.method == 'POST':
            cate_id = request.form.get('cate_id')
            art_name = request.form.get('art_name')
            describe = request.form.get('describe')
            content = request.form.get('content')
            article = Article(cate_id=cate_id, art_name=art_name, describe=describe, content=content, author=session.get('user_id'))
            db.session.add(article)
            db.session.commit()
            return 'ok'
        else:
            cate = []
            categories = Category.query.all()
            for c in categories:
                if c.parent_id == 0:
                    c.cate_name = '|--' + c.cate_name
                    cate.append(c)
                    for s in categories:
                        if s.parent_id == c.id:
                            s.cate_name = '|------' + s.cate_name
                            cate.append(s)
            return render_template('admin/add_art.html', cate=cate)
    else:
        return redirect(url_for('login'))


@app.route('/del_art/', methods=['POST'])
def del_art():
    if account() < 0:
        id = request.form.get('id')
        article = Article.query.filter(Article.id == id).first()
        if category:
            db.session.delete(article)
            db.session.commit()
            return 'ok'
        else:
            return 'no'
    else:
        return redirect(url_for('login'))


@app.route('/modify_art/', methods=['GET', 'POST'])
def modify_art():
    if account() < 0:
        if request.method == 'POST':
            id = request.form.get('id')
            cate_id = request.form.get('cate_id')
            art_name = request.form.get('art_name')
            describe = request.form.get('describe')
            content = request.form.get('content')
            art = Article.query.filter(Article.id == id).first()
            art.cate_id = cate_id
            art.art_name = art_name
            art.describe = describe
            art.content = content
            art.author = session.get('user_id')
            db.session.commit()
            return 'ok'
        else:
            id = request.args.get('id')
            art = Article.query.filter(Article.id == id).first()
            cate = []
            categories = all_cate()
            for c in categories:
                if c.parent_id == 0:
                    c.cate_name = '|--' + c.cate_name
                else:
                    c.cate_name = '|------' + c.cate_name
                cate.append(c)
            return render_template('admin/modify_art.html', cate=cate, art=art)
    else:
        return redirect(url_for('login'))


@app.route('/mar_comment/', methods=['GET'])
def mar_comment():
    if account() < 0:
        id = request.args.get('id')
        art_name = Article.query.filter(Article.id == id).first().art_name
        comments = Comment.query.filter(Comment.art_id == id).all()
        users = all_user()
        return render_template('admin/comment.html', comments=comments, art_name=art_name, users=users)
    else:
        return redirect(url_for('login'))


@app.route('/del_comment/', methods=['POST'])
def del_comment():
    if account() < 0:
        if request.method == 'POST':
            id = request.form.get('id')
            comment = Comment.query.filter(Comment.id == id).first()
            if comment:
                db.session.delete(comment)
                db.session.commit()
                return 'ok'
            else:
                return 'no'
        else:
            logout()
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/mar_user/', methods=['GET', 'POST'])
def mar_user():
    if account() < 0:
        users = all_user()
        return render_template('admin/user.html', users=users)
    else:
        return redirect(url_for('login'))


@app.route('/del_user/', methods=['POST'])
def del_user():
    if account() < 0:
        id = request.form.get('id')
        user = User.query.filter(User.id == id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return 'ok'
        else:
            return 'no'
    else:
        return redirect(url_for('login'))


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


@app.route('/favicon.ico/', methods=['GET', 'POST'])
def favicon():
    return ''


@app.route('/static/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['FileName']
        if file:
            filename = secure_filename(file.filename)
            r = random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 6)
            ss = ""
            for i in r:
                ss += i
            filename = ss + time.strftime('_%Y%m%d%H%M%S', time.localtime()) + os.path.splitext(filename)[1]
            file.save('static/media/'+filename)
            path = request.url + 'media/' + filename
            print(path)
            url = "{\"errno\": 0,\"data\": [\"" + path + "\"]}"
            return url
    return ''


if __name__ == '__main__':
    app.run()
