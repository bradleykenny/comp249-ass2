__author__ = 'Bradley Kenny'

from bottle import Bottle, template, static_file, request, response
from interface import *

app = Bottle()

@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')

@app.route('/')
def index(db):
    info = {
        'title': 'Welcome to Jobs',
        'message': 'Welcome to Jobs',
        'positions': position_list(db),
    }
    return template('index', info)

@app.route('/about/')
def about():
    info = {
        'title': 'Jobs | About',
        'message': 'About Us',
    }
    return template('about.html', info)

@app.route('/positions/<id>')
def positions(db, id):
	info = {
        'title': 'Jobs | %s' % position_get(db, int(id))[3],
        'message': 'Your next job?',
        'positions': position_get(db, int(id)),
    }
	return template('position.html', info)


if __name__ == '__main__':
    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
