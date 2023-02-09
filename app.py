#-------------------------------------------------------------------------------
# Name:			app.py
# Purpose:		"evalpsy" app
#				main app file
#
# Author:		a.goye
#
# Created:		8/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-------------------------------------------------------------------------------

from bottle import route, get, post, debug, run, template, default_app
import bottle.ext.sqlite
import os
from auth_plugin import authPlugin

onrender = 'RENDER' in os.environ
# debug(not onrender)
debug(True)

app = default_app()
app.config.update({
	'secret': "f08gOAX7ptb5eKHi1Q86YjKSEewYqchu5QCZPchmSEpFAu1IBDWqSYaGF42ir6RnxQthWNlJjvcXvYdw1e8g8zYVGVCbIGBNuHL",
	'adminids': ['1'],
	'days_relance': 15,		#delai de relance d'un patient pour réponse à une demande d'évaluation
	'days_relanceprat': 15,	#délai de relance d'un praticien pour connexion et création du mot de passe
	'days_eval1': 183,		#délai de l'inscription à la 1e demande d'évaluation par un patient
	'days_eval2': 370,		#délai de l'inscription à la 2e demande d'évaluation par un patient
})
dbplugin = bottle.ext.sqlite.Plugin(dbfile='db/evalpsy.db', keyword='db')
app.install(dbplugin)

authplugin = authPlugin(keyword='user', secret=app.config.get('secret'), 
						adminids=app.config.get('adminids'))
app.install(authplugin)
app.config['auth_plugin'] = authplugin

import home
# import admin
# import invite

if __name__ == '__main__':
	if onrender:
		hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
		run(host=hostname, port=80, debug=True)
	if not onrender:
		run(host='localhost', port=8000, debug=True, reloader=True)

# @route('/hello/<name>')
# def index(name):
	# return template('<b>Hello {{name}}</b>!', name=name)
