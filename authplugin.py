#-----------------------------------------------------------------------------
# Name:			authplugin.py
# Purpose:		"evalpsy" app
#				authentication plugin
#
# Author:		a.goye
#
# Created:		8/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

from bottle import request, redirect, makelist
from datetime import datetime
import inspect

class AuthPlugin(object):

	name = 'authplugin'

	def __init__(self, keyword='user', secret='', adminids=['1']):
		self.keyword = keyword
		self.secret = secret
		self.adminids = adminids

	def sessiondata(self):
		idtoday = request.get_cookie('session', secret=self.secret)
		if idtoday:
			id, prenom, sessiondate = idtoday.split(':')
			if sessiondate == str(datetime.date(datetime.now())):
				return {
					'id': id, 
					'prenom': prenom, 
					'isadmin': id in self.adminids
				}
		return dict()
		
	def apply(self, callback, context):
		keyword = self.keyword
		
		spec = inspect.getfullargspec(callback)
		args = makelist(spec[0]) + makelist(spec.kwonlyargs)
		if keyword not in args:
			return callback		
			
		def wrapper(*args, **kwargs):
			user = self.sessiondata()
			if user:
				kwargs[keyword] = user
				return callback(*args, **kwargs)
			else:
				redirect("/login")
				
		return wrapper
