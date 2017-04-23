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


def get_repo_names(limit=10):
	with open('repos.csv', 'a') as repos, open('since.txt', 'r+') as since_f:
		count = 0
		since = int(since_f.read())
		while since is not None and count < limit:
			repositories, since = api("repositories", since)
			since_f.seek(0)
			since_f.write(since)
			since_f.truncate()
			for repository in repositories:
				repos.write(repository['full_name']+"\n")
			print "Since %s" % since
			count += 1
	
def api(endpoint, since=0):
	data = {"since": since}
	r = requests.get("https://%s:%s@api.github.com/%s" % (username, password, endpoint), params=data)
	if r.status_code == 200:
		since = get_next_url(r.headers['Link'])
		print "Requests Remaining: %s" % r.headers['X-RateLimit-Remaining']
		return (r.json(), since)
	else:
		print r.text
		return None

if __name__ == '__main__':
    get_repo_names(limit=50000)
