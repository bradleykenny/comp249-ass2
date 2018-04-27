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


# checks for valid log in username and password
# returns true if password works for username, false for all else
def check_login(db, usernick, password):
	cur = db.cursor()
	cur.execute("SELECT * FROM users WHERE nick=?", (usernick,))
	row = cur.fetchone()
	if (row != None):
		if (row[1] == password_hash(password)):
			return True
		else:
			return False


# creates session for usernick, returns None is usernick doesn't exist
def generate_session(db, usernick):
	cur = db.cursor()
	cur.execute("SELECT * FROM users WHERE nick=?", (usernick,))
	user_row = cur.fetchone()
	if (user_row != None):
		cur.execute("SELECT * FROM sessions WHERE usernick=?", (usernick,))
		ses_row = cur.fetchone()

		if (ses_row != None):
			# checks the two users are the same in the two tables
			if (ses_row[1] == user_row[0]):
				# use existing session_id
				session_id = ses_row[0]
		else:
			# generate a NEW session_id
			session_id = str(uuid.uuid4())

			cur.execute("INSERT INTO sessions VALUES (?,?)", (session_id, usernick))
			db.commit()

		response.set_cookie(COOKIE_NAME, session_id)
		return session_id
	else:
		return None


# remove all session table entries for this user
def delete_session(db, usernick):
	cur = db.cursor()
	cur.execute("SELECT * FROM sessions WHERE usernick=?", (usernick,))
	user_row = cur.fetchone()
	if (user_row != None):
		cur.execute("DELETE FROM sessions WHERE usernick=?", (usernick,))


# try to retrieve the user from the sessions table
# return usernick or None if no valid session is present
def session_user(db):
	session_id = request.get_cookie(COOKIE_NAME)
	cur = db.cursor()
	cur.execute("SELECT * FROM sessions WHERE sessionid=?", (session_id,))
	row = cur.fetchone()
	if not row:
		return None
	return row[1]


# simply checks a username exists in the database
def correct_username(db, usernick):
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE nick=?", (usernick,))
    row = cur.fetchone()
    if row != None:
        return True
    else:
        return False
