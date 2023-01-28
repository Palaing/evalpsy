from bottle import get, post, run, template, request, response, redirect
from hmac import compare_digest as compare_hash
from helpers import *
from datetime import datetime
import bcrypt

def check_login(email, password, db):
	query = 'SELECT id, password, prenom from praticien where email=?'
	row = db.execute(query, (email,)).fetchone()
	if row and row[1] and \
		password == row[1]:
		# bcrypt.checkpw(password.encode('utf-8'),row[1].encode('utf-8')):
		return (row[0], row[2])
	return('','')

@get('/login')
def login():
	if sessionid()[0]:
		redirect('/home')
	return ftemplate('login.html', message = '')

@post('/login')
def do_login(db):
	email = request.forms.get('email')
	password = request.forms.get('password')
	idnumber, prenom = check_login(email, password, db)
	if idnumber:
		##########################
		# idnumber, prenom = ['1', 'Alain'] ################ FOR DEBUG
		##########################
		idtoday = str(idnumber) + ':' + prenom + ':' + str(datetime.date(datetime.now()))
		response.set_cookie('session', idtoday, secret=secret)
		redirect('/home')
	else:
		return ftemplate('login.html', 
			message = 'La connexion a échoué; veuillez vérifier vos identifiants')

@get('/logout')
def logout():
	response.delete_cookie('session')
	return ftemplate('login.html', 
		message = 'Vous avez bien été déconnecté')

@get('/home')
def welcome(db):
	idnumber, prenom = sessionid()
	if not idnumber:
		redirect('/login')
	return ftemplate('home.html', idnumber=idnumber, prenom=prenom)
