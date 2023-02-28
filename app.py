#-----------------------------------------------------------------------------
# Name:			app.py
# Purpose:		"evalpsy" app
#				main app file
#
# Author:		a.goye
#
# Created:		8/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

from bottle import debug, run, default_app
import bottle.ext.sqlite
import os
from authplugin import AuthPlugin
from config import secret

onrender = 'RENDER' in os.environ

app = default_app()
app.config.update({
	'base_url': os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:8000'),
	'secret': secret,		# cookies encryption key
	'adminids': ['1'],		# ids of site admins in table 'praticien'
	'days_relance': 15,		# delay before following up with a patient to evaluate
	'days_relanceprat': 15,	# delay before following up with a pratician to connect
	'days_eval1': 183,		# delay before 1st evaluation request from a patient
	'days_eval2': 370,		# delay before 2nd evaluation request from a patient
	'tmpsession_life': 1800,# lifetime of the pwd reset cookie
})

dbplugin = bottle.ext.sqlite.Plugin(dbfile='db/evalpsy.db', keyword='db')
app.install(dbplugin)

app_authplugin = AuthPlugin(keyword='user', secret = app.config.get('secret'), 
							adminids = app.config.get('adminids'))
						
app.install(app_authplugin)
app.config['authplugin'] = app_authplugin

import home
import admin
import resetpwd
import invite

if __name__ == '__main__':
	if onrender:
		hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
		run(host=hostname, port=80, debug=True)
	else:
		run(host='localhost', port=8000, debug=True, reloader=True)
