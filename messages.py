#-------------------------------------------------------------------------------
# Name:			messages.py
# Purpose:		"evalpsy" app
#				email messages to be sent to study participants and praticians
#
# Author:		a.goye
#
# Created:		6/02/2023
# Copyright:	(c) a.goye 2023
# Licence:		GPLv3
#-------------------------------------------------------------------------------

reset_password = """(Ré)initialisation de votre mot de passe
Bonjour {0},

Vous avez demandé la création ou la réinitialisation de votre mot de passe sur le site d'évaluation de la maïeusthésie.
Pour choisir votre nouveau mot de passe veuillez suivre ce lien:
{1}

Ce lien est valable 30 minutes.

Bien cordialement,
Pour l'équipe de l'étude,
Alain Goyé
+33 6 06 66 68 06 08
"""

invit_prat = """Évaluation de la maïeusthésie: connectez-vous à l'application!
Bonjour {0},

Vous avez accepté de participer à notre étude d'évaluation de la maïeusthésie, et nous vous en remercions grandement.
Pour commencer et pouvoir enregistrer des participants, créez votre compte en suivant ce lien:
{1}

Des explications sur la suite des opérations vous seront données sur le site.

Merci de votre confiance et de votre contribution!
Pour l'équipe de l'étude,
Alain Goyé
+33 6 06 66 68 06 08
"""

relance_prat = "(rappel) " + invit_prat


appel1_patient = """Évaluation de la maïeusthésie: premier appel à contribution!
Bonjour {0},

Vous avez accepté de participer à notre étude d'évaluation de la maïeusthésie, et nous vous en remercions grandement.
Voilà 6 mois que votre praticien a enregistré votre participation.
Vous êtes invité(e) à remplir un petit questionnaire en suivant ce lien:
{1}

Cela ne vous prendra pas plus de 10 minutes, et nous sera très précieux.

Merci de votre confiance et de votre contribution!
L'équipe de l'étude.

Note: 
Vous pouvez à tout moment consulter, rectifier ou supprimer vos données personnelles en notre possession, sur simple demande à: postmaster@viensatoi.fr.
Si vous ne souhaitez plus participer à cette étude et que vos données personnelles soient entièrement supprimées de notre site, veuillez suivre ce lien: {3}
"""

rappel1_patient = "(rappel) " + appel1_patient


appel2_patient = """Évaluation de la maïeusthésie: deuxième et dernier appel à contribution!
Bonjour {0},

Vous avez accepté de participer à notre étude d'évaluation de la maïeusthésie, et nous vous en remercions grandement.
Voilà 24 mois que votre praticien a enregistré votre participation.
Pour la deuxième et dernière fois, vous êtes invité(e) à remplir un petit questionnaire en suivant ce lien:
{1}

Cela ne vous prendra pas plus de 10 minutes, et nous sera très précieux.

Merci de votre confiance et de votre contribution!
L'équipe de l'étude.

Note: 
Vous pouvez à tout moment consulter, rectifier ou supprimer vos données personnelles en notre possession, sur simple demande à: postmaster@viensatoi.fr.
Si vous ne souhaitez plus participer à cette étude et que vos données personnelles soient entièrement supprimées de notre site, veuillez suivre ce lien: {3}
"""

rappel2_patient = "(rappel) " + appel2_patient
