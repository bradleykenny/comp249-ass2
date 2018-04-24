"""
Created on Mar 26, 2012

@author: steve
@student: bradley kenny [SID: 45209723]
"""

from database import *
import uuid
import requests
from bottle import response, request

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'


def check_login(db, usernick, password):
	# checks for valid log in username and password
	# returns true if password works for username, false for all else
	cur = db.cursor()
	cur.execute("SELECT * FROM users WHERE nick=?", (usernick,))
	row = cur.fetchone()
	if (row != None):
		if (row[1] == password_hash(password)):
			return True
		else:
			return False

def generate_session(db, usernick):
	# creates session for usernick, returns None is usernick doesn't exist
	cur = db.cursor()
	cur.execute("SELECT * FROM users WHERE nick=?", (usernick,))
	user_row = cur.fetchone()
	if (user_row != None):
		cur.execute("SELECT * FROM sessions WHERE usernick=?", (usernick,))
		ses_row = cur.fetchone()

		if (ses_row != None):
			if (ses_row[1] == user_row[0]):
				session_id = ses_row[0]
		else:
			session_id = str(uuid.uuid4())
			cur.execute("INSERT INTO sessions VALUES (?,?)", (session_id, usernick))
			db.commit()

		response.set_cookie(COOKIE_NAME, session_id)
		return session_id
	else:
		return None


def delete_session(db, usernick):
    # remove all session table entries for this user
	cur = db.cursor()
	cur.execute("SELECT * FROM sessions WHERE usernick=?", (usernick,))
	user_row = cur.fetchone()
	if (user_row != None):
		cur.execute("DELETE FROM sessions WHERE usernick=?", (usernick,))


def session_user(db):
    # try to retrieve the user from the sessions table
	# return usernick or None if no valid session is present
	session_id = request.get_cookie(COOKIE_NAME)
	cur = db.cursor()
	cur.execute("SELECT * FROM sessions WHERE sessionid=?", (session_id,))
	row = cur.fetchone()
	if not row:
		return None
	return row[1]
