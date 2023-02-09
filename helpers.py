#-------------------------------------------------------------------------------
# Name:			app.py
# Purpose:		"evalpsy" app
#				utility functions
#
# Author:		a.goye
#
# Created:		8/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-------------------------------------------------------------------------------

from bottle import template, abort

def ensureadmin(user):
	if not user['isadmin']:
		abort(401)

def log(msg):
	with open('evalpsy.log', 'a', encoding='utf-8') as logfile:
		logfile.write('\n' + msg)
	return msg

def ftemplate(file,**kwargs):
	with open('vues/' + file, 'r', encoding='utf-8') as template_file:
		tempstring = template_file.read()
	return template(tempstring,kwargs)