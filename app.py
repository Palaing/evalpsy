from bottle import route, get, post, debug, run, template, default_app
import bottle.ext.sqlite
import os
import home

onrender = 'RENDER' in os.environ
# debug(not onrender)
debug(TRUE)

plugin = bottle.ext.sqlite.Plugin(dbfile='db/evalpsy.db', keyword='db')
# app.install(plugin)

if __name__ == '__main__':
	if onrender:
		hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
		run(host=hostname, port=80)
	if not onrender:
		run(host='localhost', port=8000, debug=True, reloader=True, plugins=(plugin,))

@route('/hello/<name>')
def index(name):
	return template('<b>Hello {{name}}</b>!', name=name)

# to run on render with gunicorn:	
app = default_app()
