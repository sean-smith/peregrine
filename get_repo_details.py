import requests
from pprint import pprint
from credentials import username, password
import collections
import pandas as pd

def get_languages(repo):
	languages = api('repos/%s/languages' % repo)
	stats = collections.Counter(languages)
	return (len(languages), stats.most_common(3))

def get_repo_deets(limit=10, in_done=True):
	count = 0
	with open('repos.csv', 'r') as repos, \
	open('failed.csv', 'a') as failed, \
	open('last.txt', 'r+') as last:
		last_done = last.read();
		print "last_done = [%s]" %last_done
		for repo in repos:
			# Strip off trailing \n
			repo = repo[:-1]
			if in_done:
				if last_done in repo:
					in_done = False
				print "Skipping [%s]" % repo
				continue
			if count >= limit:
				break
			count += 1
			try:
				# repo = 'facebook/react-native'
				json = api("repos/%s" % repo)
				if json is not None:
					d = {}
					d['forks'] = json['forks_count']
					d['stars'] = json['stargazers_count']
					d['watchers'] = json['subscribers_count']
					d['owner'] = json['owner']['login']
					d['type'] = json['owner']['type']
					d['issues'] = json['open_issues_count']
					d['created_at'] = json['created_at']
					d['name'] = repo
					d['language_1'] = json['language']
					d['description'] = json['description']
					d['size'] = json['size']
					d['open_issues_count'] = json['open_issues_count']
					d['pushed_at'] = json['pushed_at']
					d['updated_at'] = json['updated_at']
					num_languages, languages = get_languages(repo)
					i = 1
					for lang, size in languages:
						d['language_%d' % i] = lang
						d['language_%d_size' % i] = size
						i += 1
					d['num_languages'] = num_languages
					# pprint(d)
				else:
					raise Exception('Nonetype returned from api call')
				# Write to file:
				df = pd.DataFrame([d], columns=['name', 'owner', 'watchers', 'stars', 'forks', 'type', 'issues', 'created_at', 'pushed_at', 'updated_at', 'size', 'open_issues_count', 'description', 'num_languages', 'language_1', 'language_1_size', 'language_2', 'language_2_size', 'language_3', 'language_3_size'])
				with open('github_data.csv', 'a') as f:
					df.to_csv(f, encoding='utf-8', header=f.tell()==0, index=False)
					print repo
					# Write new last seen
					last.seek(0)
					last.write(repo)
					last.truncate()
			except Exception as e:
				print "%s failed with error %s" % (repo, e)
				failed.write(repo+'\n')

			
def api(endpoint):
	r = requests.get("https://%s:%s@api.github.com/%s" % (username, password, endpoint))
	if r.status_code == 200:
		print "Requests Remaining: %s" % r.headers['X-RateLimit-Remaining']
		return r.json()
	else:
		print "[%d] <%s>\n%s" %(r.status_code, r.url, r.text)
		return None

if __name__ == '__main__':
	get_repo_deets(limit=2500)
