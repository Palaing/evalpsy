#-------------------------------------------------------------------------------
# Name:			config_template.py
# Purpose:		"evalpsy" app
#				show structure of config.py file: confidential configuration data
#
# Author:		a.goye
#
# Created:		ç/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-------------------------------------------------------------------------------

# secret key for cookies encryption
secret = "a_very_secret_phrase_to_encode_cookies"

# smtp data for sending emails,
# plus default 'to' and 'from' mail addresses
mail = {
	'host':	'ssl.mysmtpserver.com',
	'port':	587,
	'id':	'my_id_on_ssl.mysmtpserver.com',
	'pwd': 	'my_password_on_ssl.mysmtpserver.com',
	'to': 	'defaultreccipient@someserver.com',
	'from':	'defaultsender@someserver.com',
}