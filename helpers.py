from bottle import template, request
from datetime import datetime

secret = "f08gOAX7ptb5eKHi1Q86YjKSEewYqchu5QCZPchmSEpFAu1IBDWqSYaGF42ir6RnxQthWNlJjvcXvYdw1e8g8zYVGVCbIGBNuHL"

def log(msg):
	with open('form.log', 'a', encoding='utf-8') as logfile:
		logfile.write('\n' + msg)
	return msg

def sessionid():
	idtoday = request.get_cookie('session', secret=secret)
	if idtoday:
		userid, prenom, sessiondate = idtoday.split(':')
		if sessiondate == str(datetime.date(datetime.now())):
			return (userid, prenom)
	return ('','')
	# if userid and sessiondate == str(datetime.date(datetime.now())):
		# redirect('/home')
	# else:
		# return ftemplate('login.html', message = 'Votre session est échue. Veuillez vous reconnecter')

def tempfile(file):
	with open('vues/' + file, 'r', encoding='utf-8') as template_file:
		tempstring = template_file.read()
	return tempstring

def ftemplate(file,**kwargs):
	return template(tempfile(file),kwargs)