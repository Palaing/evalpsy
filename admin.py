#-----------------------------------------------------------------------------
# Name:			admin.py
# Purpose:		"evalpsy" app
#				administrator routes
#
# Author:		a.goye
#
# Created:		8/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

from bottle import get, post, request
from datetime import datetime
from helpers import ensureadmin, ftemplate, validmail
import messages as msgs
import re

@get('/addprat')
def addprat(user):
	ensureadmin(user)
	return ftemplate('addprat.html', user=user)

@post('/addprat')
def do_addprat(user, db):
	ensureadmin(user)
	cur = db.cursor()
	messages = []
	emails = set(request.forms.getunicode('emails').split())
	goodmails, badmails = [], []
	for email in emails:
		(badmails, goodmails)[validmail(email)].append(email)
	if badmails:
		messages.append(msgs.invalid_mails + ', '.join(badmails))
		
	cur.execute('SELECT email FROM praticien')
	dbmails = [row[0] for row in cur.fetchall()]
	newmails, oldmails = [], []
	for email in goodmails:
		(newmails, oldmails)[email in dbmails].append(email)
	if oldmails:
		messages.append(msgs.existing_mails + ', '.join(oldmails))
		
	query = 'INSERT INTO praticien (email) VALUES (?);'
	cur.executemany(query, [(row,) for row in newmails])
	
	cur.execute('SELECT email FROM praticien')
	dbmails = [row[0] for row in cur.fetchall()]
	missing = [email for email in newmails if email not in dbmails]
	if missing:
		messages.append(msgs.unrecorded_mails + ', '.join(missing))
	return ftemplate('addprat.html', user=user, 
		message = '<br>'.join(messages))

@get('/showprat')
def showprat(user, db):
	ensureadmin(user)
	query = """SELECT pr.email, pr.dateappel, pr.daterappel, pr.dateconnecte,
		COUNT(pa.id) as participants
		FROM praticien as pr 
		LEFT JOIN participant as pa ON pr.id = praticien_id
		GROUP BY pr.email"""
	cur = db.execute(query)
	praticiens = cur.fetchall()
	return ftemplate('pratlist.html', user=user, praticiens=praticiens)
	