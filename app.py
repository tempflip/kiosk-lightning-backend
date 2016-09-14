from flask import Flask, send_from_directory, request, redirect
import requests
import urllib
import os

app = Flask(__name__)

CONSUMER_KEY = '3MVG9Km_cBLhsuPwN4mdHKHsxEfFSw9ezKAKdrUMeMeViBZAUF6Nbv9L_M5SrZ5LltrdyUx2KyXIJXEByxHyx'
SECRET_KEY = '4529370390844900674';
AUTH_URL = 'https://login.salesforce.com/services/oauth2/authorize'

if ('PORT' in os.environ):
	HOST_URL = 'https://blackthorn-kiosk.herokuapp.com'
	CALLBACK_URL = HOST_URL + '/oauth';
	PORT = os.environ.get('PORT')
else:
	HOST_URL = 'http://localhost:8000'
	CALLBACK_URL = HOST_URL + '/oauth'
	PORT = 8000

print ('running on port ' + PORT)

@app.route('/public/<filename>')
def public(filename):
	return send_from_directory('', filename)

@app.route('/fonts/webfonts/<filename>')
def fonts(filename):
	return send_from_directory('', filename)

@app.route('/webview')
def webview():
	return send_from_directory('', 'webview.html')

@app.route('/auth')
def auth():

	d = {
	'response_type' : 'code',
	'client_id' : CONSUMER_KEY,
	'redirect_uri' : CALLBACK_URL
	}

	url = AUTH_URL + '?' + urllib.urlencode(d)
	return redirect(url)

@app.route('/oauth')
def oauth():
	code = request.args.get('code')

	data = { 'code' : code,
	'grant_type' : 'authorization_code',
	'client_id' : CONSUMER_KEY,
	'client_secret' : SECRET_KEY,
	'redirect_uri' : CALLBACK_URL
	}
	r = requests.post('https://login.salesforce.com/services/oauth2/token', data)
	print r.json()['access_token']

	return redirect(HOST_URL + '/webview?token=' + r.json()['access_token']);





if __name__ == "__main__":
    app.run(port=PORT, host='0.0.0.0')

