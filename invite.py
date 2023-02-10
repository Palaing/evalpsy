#-------------------------------------------------------------------------------
# Name:			invite.py
# Purpose:		"evalpsy" app
#				timely send invitation/reminder messages to participants and praticians
#
# Author:		a.goye
#
# Created:		6/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-------------------------------------------------------------------------------

from bottle import get, post, request, response, redirect, error
from datetime import datetime, timedelta
import messages as msgs
from sendmail import sendmail
from helpers import log

@get('/invite')
def invite(db):	
	# ----- Praticiens non encore connectés ni invités 2 fois ------
	query = 'SELECT email, dateappel, prenom FROM praticien 	\
			WHERE dateconnecte IS NULL					\
			AND daterappel IS NULL'
	cur = db.execute(query)
	praticiens = cur.fetchall()
	nouveaux, anciens = [], []
	for prat in praticiens:
		(anciens, nouveaux)[not prat[1]].append(prat)

	# ----- Praticiens jamais invités ------
	for prat in nouveaux:
		res = sendmail(msgs.invit_prat.format(prat[2],''))
		if res == "success":
			updatequery = 'UPDATE praticien SET dateappel=?'
			datestr = datetime.now().strftime('%Y-%m-%d')
			cur.execute(updatequery, (datestr,))
			log(str(datetime.now()) + ': sent invit_prat message to: ' + prat[0])
		else: 
			log(str(datetime.now()) + ': invit_prat message could not be sent to: ' + prat[0])
			
	# ----- Praticiens invités depuis plus de (days_relanceprat) jours ------
	for prat in anciens:
		dateappel = datetime.strptime(prat[1], '%Y-%m-%d') 
		delai = request.app.config['days_relanceprat']
		if datetime.now() - dateappel > timedelta(delai):
			res = sendmail(msgs.relance_prat.format(prat[2],''))
			if res == "success":
				updatequery = 'UPDATE praticien SET daterappel=?'
				datestr =  datetime.now().strftime('%Y-%m-%d')
				cur.execute(updatequery, (datestr,))
				log(str(datetime.now()) + ': sent relance_prat message to: ' + prat[0])
			else: 
				log(str(datetime.now()) + ': relance_prat message could not be sent to: ' + prat[0])

	# ----- Patients-évaluateurs... ------
