__author__ = 'Bradley Kenny'

from bottle import Bottle, template, static_file, request, response, redirect
from interface import *
from users import *

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
		'log_in':  loginform_ornot(db),
    }
    return template('index', info)


@app.route('/about/')
def about(db):
    info = {
        'title': 'Jobs | About',
        'message': 'About Us',
		'log_in': loginform_ornot(db),
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


@app.route('/login', method="POST")
def login(db):
	nick = request.forms.get('nick')
	password = request.forms.get('password')
	if check_login(db, nick, password):
		generate_session(db, nick)
		return redirect('/')
	else:
		return redirect('/')


@app.route('/logout')
def logout(db):
	nick = session_user(db)
	delete_session(db, nick)
	return redirect('/')


# ===== HELPER METHODS =====

def loginform_ornot(db):
	name = session_user(db)
	if name != None:
		return ("""
			<form action="/logout" id="logoutform">
				<p>Logged in as <b><i>%s</i></b></p>
				<input type='submit' value="Logout"/>
			</form>
			""" % name)
	else:
		return("""
			<form action="/login" id="loginform" method="POST">
				<input type="text" name="nick" placeholder="Username"/>
				<input type="password" name="password" placeholder="Password"/>
				<input type='submit' value="Login"/>
			</form>
			""")


if __name__ == '__main__':
    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
