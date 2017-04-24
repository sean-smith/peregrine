import requests
from credentials import client_id, client_secret
import urllib
from flask import Flask, request
from pprint import pprint

access_token_url = "https://github.com/login/oauth/access_token"
authorize_url = "https://github.com/login/oauth/authorize"


data = {
	"client_id": client_id,
	"redirect_uri": "http://localhost:8080",
	"scope": "",
	"state": "supersecretstate"
}

print("Go to:")
print("%s?%s" % (authorize_url, urllib.urlencode(data)))
print("Waiting for response...")

app = Flask(__name__)

@app.route("/")
def get_access_token():
	# parse code
	code = request.args.get('code')
	print code
	data = {
		"client_id": client_id,
		"client_secret": client_secret,
		"code": code
	}
	headers = {
		"Accept": "application/json"
	}
	r = requests.post(access_token_url, data=data, headers=headers)
	if r.status_code == 200:
		return str(r.json())

if __name__ == "__main__":
    app.run('localhost', 8080)
