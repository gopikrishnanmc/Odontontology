from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from settings import USER_EMAIL, USER_PASSWORD
from functools import wraps

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('settings')

db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(50), default='Gopikrishnan M.C.')
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
@app.route('/index')
def index():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            if email == USER_EMAIL and password == USER_PASSWORD:
                session['username'] = email
                return redirect(url_for('add'))
            else:
                error = "Invalid credentials. Try again."
        return render_template('login.html', error=error)
    except Exception as e:
        flash(e)
        return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.filter_by(id=post_id).one()
    return render_template('post.html', title=post.title, post=post)


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/dental_clinics_1')
def show_dental_clinics():
    return render_template('map_1.html', title='Dental practices')


# @app.route('/maps')
# def maps_intro():
#     return render_template('maps_intro.html', title='Maps')


@app.route('/add')
@login_required
def add():
    return render_template('add.html', title='Add')


@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    subtitle = request.form['subtitle']
    content = request.form['content']
    post = BlogPost(title=title, subtitle=subtitle, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404')


if __name__ == '__main__':
    app.run(debug=True)
