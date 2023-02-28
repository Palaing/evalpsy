#-----------------------------------------------------------------------------
# Name:			invite.py
# Purpose:		"evalpsy" app
#				timely send invitation/reminder messages 
#				to participants and praticians
#
# Author:		a.goye
#
# Created:		6/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-----------------------------------------------------------------------------

from bottle import get, request
from datetime import datetime, timedelta
import messages as msgs
from sendmail import sendmail
from helpers import log

@get('/invite')
def invite(db):	
	# ----- Praticians not yet connected or invited twice ------
	query = """SELECT email, dateappel, prenom FROM praticien
			WHERE dateconnecte IS NULL
			AND daterappel IS NULL"""
	cur = db.execute(query)
	praticiens = cur.fetchall()
	nouveaux, anciens = [], []
	for prat in praticiens:
		(anciens, nouveaux)[not prat[1]].append(prat)

	# ----- Praticians never connected ------
	for prat in nouveaux:
		res = sendmail(msgs.invit_prat.format(prat[2],''))
		if res == "success":
			updatequery = 'UPDATE praticien SET dateappel=?'
			datestr = datetime.now().strftime('%Y-%m-%d')
			cur.execute(updatequery, (datestr,))
			log(str(datetime.now()) 
				+ ': sent invit_prat message to: ' + prat[0])
		else: 
			log(str(datetime.now()) 
				+ ': invit_prat message NOT sent to: ' + prat[0])
			
	# ----- Praticiens invited since more than (days_relanceprat) days ---
	for prat in anciens:
		dateappel = datetime.strptime(prat[1], '%Y-%m-%d') 
		delai = request.app.config['days_relanceprat']
		if datetime.now() - dateappel > timedelta(delai):
			res = sendmail(msgs.relance_prat.format(prat[2],''))
			if res == "success":
				updatequery = 'UPDATE praticien SET daterappel=?'
				datestr =  datetime.now().strftime('%Y-%m-%d')
				cur.execute(updatequery, (datestr,))
				log(str(datetime.now()) 
					+ ': sent relance_prat message to: ' + prat[0])
			else: 
				log(str(datetime.now()) 
					+ ': relance_prat message NOT sent to: ' + prat[0])

	# ----- Participants... ------
