"""
Database Model interface for the COMP249 Web Application assignment

@author: steve cassidy
@student: bradley kenny [45209723]
"""

import sqlite3

def position_list(db, limit=10):
	# return a list of positions ordered by date
	# return at most limit positions (default 10)
	# returns a list of tuples  (id, timestamp, owner, title, location, company, description)
	cursor = db.cursor()
	# result is a 2d array: result[row][column]
	# 0=id, 1=timestamp, 2=owner, 3=title, 4=location, 5=company, 6=description
	cursor.execute("SELECT * FROM positions ORDER BY date(timestamp) desc")
	rows = cursor.fetchmany(limit)

	result = []
	for row in rows:
		result.append(row)

	return result


def position_get(db, id):
	# return the details of the position with the given id
	# or None if there is no position with this id
	# returns a tuple (id, timestamp, owner, title, location, company, description)
	cursor = db.cursor()
	cursor.execute("SELECT * FROM positions")
	rows = cursor.fetchall()

	result = None
	for row in rows:
		if row[0] == id:
			result = row

	return result


def position_add(db, usernick, title, location, company, description):
	# add a new post to the database.
	# the date of the post will be the current time and date.
	# only add the record if usernick matches an existing user
	# return True if the record was added, False if not.
	cursor = db.cursor()
	cursor.execute("SELECT nick FROM users")

	rows = cursor.fetchall()
	exists = False
	for row in rows:
		if row[0] == usernick:
			exists = True

	# if username exists, insert the values into the table
	if exists == True:
		sql = """INSERT INTO positions(timestamp, owner, title, location, company, description) VALUES (datetime(),?,?,?,?,?)"""
		cursor.execute(sql, (usernick, title, location, company, description))
		db.commit()
		return True
	# if the username doesn't exist, nothing will happen
	elif exists == False:
		return False
