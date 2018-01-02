from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'gopi'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie is cool'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/dental_clinics_1')
def show_dental_clinics():
    return render_template('map_1.html', title='Dental practices')


@app.route('/maps')
def maps_intro():
    return render_template('maps_intro.html', title='Maps')
