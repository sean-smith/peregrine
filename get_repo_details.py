import requests
from pprint import pprint
from credentials import username, password
import re

def get_next_url(link_header):
	match = re.search(r"since=(\d+)", link_header)
	if match:
		return match.group(1)
	print link_header
	return None


def get_repo_deets(limit=10):
	count = 0
	with open('repos.csv', 'r') as repos:
		for repo in repos:
			if count > limit:
				break
			# Strip off trailing \n
			repo = repo[:-1]
			json = api("repos/%s" % repo)
			if json is not None:
				pprint(json)
			count += 1
			
	
def api(endpoint, since=0):
	r = requests.get("https://%s:%s@api.github.com/%s" % (username, password, endpoint))
	print r.url
	if r.status_code == 200:
		print "Requests Remaining: %s" % r.headers['X-RateLimit-Remaining']
		return r.json()
	else:
		print r.url
		print r.text
		return None

if __name__ == '__main__':
    get_repo_deets(limit=5)
