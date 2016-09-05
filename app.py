from flask import Flask, send_from_directory, request, redirect
import requests
import urllib
import os

app = Flask(__name__)

CONSUMER_KEY = '3MVG9Km_cBLhsuPwN4mdHKHsxEfFSw9ezKAKdrUMeMeViBZAUF6Nbv9L_M5SrZ5LltrdyUx2KyXIJXEByxHyx'
SECRET_KEY = '4529370390844900674';
AUTH_URL = 'https://login.salesforce.com/services/oauth2/authorize'

if ('PORT' in os.environ):
	CALLBACK_URL = 'http://blackthorn-kiosk.herokuapp.com/';
	PORT = os.environ.get('PORT')
else:
	CALLBACK_URL = 'http://localhost:8000/oauth'
	PORT = 8000


@app.route('/webview')
def webview():
	return 'hali maki'
	return send_from_directory('', 'webview.html')


@app.route('/auth')
def auth():

	d = {
	'response_type' : 'code',
	'client_id' : CONSUMER_KEY,
	'redirect_uri' : CALLBACK_URL
	}

	url = AUTH_URL + '?' + urllib.urlencode(d)
	#url += '?response_type=code'
	#url += '&client_id=' + urllib.urlencode(CONSUMER_KEY)
	#url += '&redirect_uri=' + urllib.urlencode(CALLBACK_URL)
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

	return redirect('/webview?token=' + r.json()['access_token']);

# https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=<your_client_id>&redirect_uri=<your_redirect_uri>

if __name__ == "__main__":
    app.run(port=PORT)

