# Readme for evalpsy

## Purpose
A small application designed to manage a study to evaluate the efficiency of an approach of psychotherapy called maïeusthesis - which means "the art of being sensitive (aisthêsis in Greek) to the birth (Maïa is the Greek goddess of childbirth) of parts of oneself".
Maïeusthesis, or maïeusthésie in French, is a humanistic psychotherapy approach developped by Thierry Tournebise - see https://www.maieusthesie.com/.

As this approach is quite recent and its diffusion still restricted, the study aims at demonstrating its efficiency in order to widen its benefits to a larger number of people.

## Study protocol
The study is designed to run as follows:
1. the animation group enrols volunteer praticians
1. praticians enrol volunteer clients with minimal contact data and information on the purpose of their consultation
1. at predefined intervals after enrolment time, volunteer clients will receive emails inviting them to fill an evaluation form
The evaluation form itself is not managed by this application. It is supposed to be hosted on some cloud survey service

## App structure
The app is developed in Python with the Bottle framework.
It runs as a wsgi app, which can be hosted on render.com.

It requires the following modules:
* bcrypt==4.0.1
* bottle==0.12.23
* bottle-sqlite==0.2.0

There are 2 levels of user:
* *praticians* can set their password, log in, register clients and list their registered clients
* *admins* can also register praticians and list all praticians with their participation status

Data are stored in a sqlite database with 3 tables:
* *praticien* for praticians,
* *participant* for clients,
* *token* for tokens sent in password-initialization emails

## Main files

### app.py
Creates the bottle app, configures it and starts the server (gunicorn on render)

### home.py
Accessible to all registered users. Contains all routes to:
* login and logout
* add a participant
* list participants
* redirect on 401 and 404 errors

### resetpwd.py
Accessible to all registered users. Contains all routes to set or reset their password, in the following classical stages:
1. user sends password reset request with email address
1. server sends a reset link to their mailbox
1. user follows link and chooses new password
1. the new password is stored and active

### admin.py
Accessible only to admin users. Contains all routes to:
* add a user (i.e. pratician)
* list users (i.e. praticians)

## Other files
* *helpers.py*: utility functions
* *authplugin.py*: authentication plugin for restricted pages
* *sendmail.py*: a smtplib.SMTP wrapper to simplify sending email messages

## Configuration files
* *config.py*: confidential configuration data - see config_template.py
* *messages.py*: text of email messages sent by the app

