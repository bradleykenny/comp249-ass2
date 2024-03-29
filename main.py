__author__ = 'Bradley Kenny'

from bottle import Bottle, template, static_file, request, response, redirect, HTTPResponse
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
        'job_post': newjobform_ornot(db),
    }
    return template('index', info)


@app.route('/about')
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
        'log_in': loginform_ornot(db),
    }
    return template('position.html', info)


@app.route('/all_positions')
def all_positions(db):
    info = {
        'title': 'Jobs | All Positions',
        'message': 'Available Jobs',
        'positions': position_list_all(db),
        'log_in': loginform_ornot(db),
    }
    return template('all_positions.html', info)


@app.route('/login', method="POST")
def login(db):
    nick = request.forms.get('nick')
    password = request.forms.get('password')
    if check_login(db, nick, password):
        generate_session(db, nick)
        return redirect('/')
    elif correct_username(db, nick):
        response.status = 200
        return wrong_pw(db)
    else:
        return redirect('/')


# called in login() when password incorrect
def wrong_pw(db):
    info = {
        'title': 'Jobs | Wrong Password',
        'message': 'Wrong Password',
        'log_in': "",
    }
    return template('wrong_pw.html', info)


@app.route('/logout')
def logout(db):
    nick = session_user(db)
    delete_session(db, nick)
    return redirect('/', 302)


@app.route('/post', method="POST")
def post(db):
    user = session_user(db)
    title = request.forms.get('title')
    location = request.forms.get('location')
    company = request.forms.get('company')
    description = request.forms.get('description')
    if user != None:
        position_add(db, user, title, location, company, description)
        return redirect('/')
    else:
        return redirect('/')


# ===== HELPER METHODS =====

# if the user is logged in, this returns the 'logoutform'
# however, if no one is logged in, it will return a log in form
def loginform_ornot(db):
    name = session_user(db)
    if name != None:
        return ("""
            <form action="/logout" id="logoutform">
                <p>Logged in as %s</p>
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


# if someone is logged in, returns a form to create a new job
# if no one is logged in, returns an empty string AKA nothing
def newjobform_ornot(db):
    name = session_user(db)
    if name != None:
        return ("""
            <h1 style="font-size: 20px; font-family: 'Merriweather';">POST A NEW JOB</h1>
            <div id="postform_card" class="card">
                <form action="/post" id="postform" method="POST">
                    <input type="text" name="title" placeholder="Title" class="post_title"/>
                    <input type="text" name="location" placeholder="Location" class="post_location"/>
                    <input type="text" name="company" placeholder="Company" class="post_company"/>
                    <textarea name="description" placeholder="Description" class="post_description"></textarea>
                    <input type='submit' value="Post" class="button"/>
                </form>
            </div>
            """)
    else:
        return("")


if __name__ == '__main__':
    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
