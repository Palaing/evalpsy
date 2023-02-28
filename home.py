#-----------------------------------------------------------------------------
# Name:			app.py
# Purpose:		"evalpsy" app
#				normal users (praticians) routes
#
# Author:		a.goye
#
# Created:		8/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

from bottle import get, post, request, response, redirect, error
from datetime import datetime
from helpers import ensureadmin, ftemplate
import messages as msgs
import bcrypt
import re

def check_pwd(email, password, db):
	query = 'SELECT id, password, prenom FROM praticien WHERE email=?'
	row = db.execute(query, (email,)).fetchone()
	if row and row[1] and \
		bcrypt.checkpw(password.encode('utf-8'),row[1]):
		return (row[0], row[2])
	return('','')

@get('/login')
def login():	
	if request.app.config['authplugin'].sessiondata():
		redirect('/add')
	return ftemplate('login.html', redirecturl='/add')

@post('/login')
def do_login(db):
	email = request.forms.getunicode('email')
	password = request.forms.getunicode('password')
	redirecturl = request.forms.getunicode('redirecturl', '/add')
	id, prenom = check_pwd(email, password, db)
	if id:
		idtoday = ':'.join([str(id), prenom, 
							str(datetime.date(datetime.now()))])
		response.set_cookie('session', idtoday, 
							secret = request.app.config.get('secret'))
		redirect(redirecturl)
	else:
		return ftemplate('login.html', message = msgs.connexion_failed,
						redirecturl = redirecturl)

@get('/logout')
def logout():
	response.delete_cookie('session')
	return ftemplate('login.html', 
		message = msgs.logout_ok, redirecturl='/add')

@get('/')
@get('/add')
def add(user):
	return ftemplate('addpatient.html', user=user)

@post('/add')
def do_add(user, db):

	cur = db.cursor()
	email = request.forms.getunicode('email')
	if not re.match(r'[^@]+@[^@]+\.[^@]+', email):	
		return ftemplate('addpatient.html', user=user,
			message = msgs.request_validmail)
	
	checkquery = 'SELECT id FROM participant WHERE email=?'
	cur.execute(checkquery, (email,))
	if len(cur.fetchall()) > 0:
		return ftemplate('addpatient.html', user=user,
			message = msgs.mail_exists)
	
	# request.forms.get doesn't return unicode, using request.forms.getunicode
	prenom = request.forms.getunicode('prenom')
	nom = request.forms.getunicode('nom')
	telephone = request.forms.getunicode('telephone')
	newpatient = request.forms.getunicode('newpatient')
	symptome = request.forms.getunicode('symptome')
	intensite = request.forms.getunicode('intensite')
	datein = str(datetime.date(datetime.now()))
	query = """INSERT INTO participant
		(prenom, nom, telephone, email, newpatient, datein,
			symptome, intensite, praticien_id)
		VALUES (?,?,?,?,?,?,?,?,?);"""
	cur.execute(query, (prenom, nom, telephone, email, newpatient, datein,
						symptome, intensite, user['id'],))

	cur.execute(checkquery, (email,))
	if len(cur.fetchall()) < 1:
		return ftemplate('addpatient.html', user=user,
			message = msgs.recording_failed)
	return ftemplate('addpatient.html', user=user, 
			message = msgs.recording_success)

@get('/show')
def show(user, db):
	query = """SELECT nom,  prenom,  email,  telephone,  datein 
		FROM participant WHERE praticien_id=?"""
	cur = db.execute(query, (user['id'],))
	participants = cur.fetchall()
	return ftemplate('patientlist.html', user=user, participants=participants)
	
@error(401)
def error401(url):
	return ftemplate('401.html')
	
@error(404)
def error404(error):
	return ftemplate('404.html')
