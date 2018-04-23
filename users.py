"""
Created on Mar 26, 2012

@author: steve
"""

from database import *

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'


def check_login(db, usernick, password):
	cur = db.cursor()
	cur.execute("SELECT * FROM users WHERE nick=?", (usernick,))
	row = cur.fetchone()
	if (row != None):
		if (row[1] == password_hash(password)):
			return True
		else:
			return False

def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """


def delete_session(db, usernick):
    """remove all session table entries for this user"""


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
