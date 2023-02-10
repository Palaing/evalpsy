#-------------------------------------------------------------------------------
# Name:			resetpwd.py
# Purpose:		"evalpsy" app
#				password reset routes
#
# Author:		a.goye
#
# Created:		8/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-------------------------------------------------------------------------------

from bottle import request, response, get, post
from helpers import log, ftemplate
import re
import hashlib
import bcrypt
from datetime import datetime, timedelta
import messages as msgs
from sendmail import sendmail

# validate a password with min length 6 and max length 20,
# at least 1 digit, 1 upcase and 1 lowcase letter, 1 special character
def validpwd(password):
	pattern = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
	return re.search(pattern, password)

@get('/forgotpwd')
def forgotpwd():
	return ftemplate('forgotpwd.html')

@post('/forgotpwd')
def do_forgotpwd(db):
	# get id from given email, exit if none
	email = request.forms.getunicode('email')
	cur = db.execute('SELECT id, prenom FROM praticien WHERE email=?', (email,))
	prat = cur.fetchone()
	if not (prat and prat[0]):
		return ftemplate('login.html', message='Si vous avez fourni une adresse mail valide, un message vous a été envoyé. Veuillez consulter votre messagerie')
	id = prat[0]
	
	# save a token and date for this id
	cur.execute('DELETE FROM token WHERE praticien_id=?', (id,))
	exp = datetime.now() + timedelta(minutes=30)
	token = hashlib.md5(str(exp).encode()).hexdigest()
	query = 'INSERT INTO token (praticien_id, exp_datetime, token) VALUES (?,?,?);'
	cur.execute(query, (id, exp.strftime('%Y-%m-%d %H:%M:%S'), token,))
	
	# verify
	cur.execute('SELECT praticien_id FROM token WHERE praticien_id=?', (id,))
	if len(cur.fetchall()) < 1:
		return ftemplate('login.html', message="Une erreur s'est produite")

	# send link by mail to user
	link = request.app.config['base_url'] + '/resetpwd/' + str(id) + '/' + token
	# res = sendmail(msgs.reset_password.format(prat[1],link), email)
	res = sendmail(msgs.reset_password.format(prat[1], link))
	if res == "success":
		log(str(datetime.now()) + ': sent password-reset link to ' + email)
	else: 
		log(str(datetime.now()) + ': failed to send password-reset link to ' + email)
	return ftemplate('login.html', message='Si vous avez fourni une adresse mail valide, un message vous a été envoyé. Veuillez consulter votre messagerie.')
	
@get('/resetpwd/<id>/<token>')
def resetpwd(id, token, db):
	# check token and its expiry date
	query = 'SELECT exp_datetime, token FROM token WHERE praticien_id=?'
	cur = db.execute(query, (id,))
	data = cur.fetchone()
	if not data or token != data[1]:
		return ftemplate('login.html', message='Une erreur s\'est produite. Le lien utilisé est invalide.')
	if datetime.now() > datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S'):
		return ftemplate('login.html', message='Le lien de réinitialisation du mot de passe a expiré.')

	# send id in tmp cookie
	content = str(id) + ':' + str(datetime.date(datetime.now()))
	response.set_cookie('tmpsession', content, secret=request.app.config.get('secret'))

	# send choose-password page
	return ftemplate('resetpwd.html')
	
@post('/resetpwd')
def do_resetpwd(db):
	# check tmp cookie
	content = request.get_cookie('tmpsession', secret=request.app.config.get('secret'))
	if not content:
		return ftemplate('login.html', message='Une erreur s\'est produite, le mot de passe n\'a pas été enregistré.')
	id, sessiondate = content.split(':')
	if sessiondate != str(datetime.date(datetime.now())):
		return ftemplate('login.html', message='Le délai de réinitialisation du mot de passe a expiré.')
			
	# encode and store new password
	password = request.forms.getunicode('password')
	if not validpwd(password):
		return ftemplate('forgotpwd.html', message='Le mot de passe fourni n\'est pas valide. Veuillez réessayer.')
	pwd = password.encode('utf-8')
	hashedpwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
	
	query = 'UPDATE praticien SET password=?, dateconnecte=? WHERE id=?'
	cur = db.execute(query, (hashedpwd, str(datetime.date(datetime.now())), id,))
	
	# verify
	cur.execute('SELECT password, dateconnecte FROM praticien WHERE id=?', (id,))
	data = cur.fetchone()
	if not (data and data[0] and data[1]):
		return ftemplate('login.html', message='Une erreur s\'est produite. Le mot de passe n\'a pas été enregistré.')

	# clean and send login page
	cur.execute('DELETE FROM token WHERE praticien_id=?', (id,))
	response.delete_cookie('tmpsession')
	return ftemplate('login.html', message='Votre nouveau mot de passe a été enregistré avec succès.')
