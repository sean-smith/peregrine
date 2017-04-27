import requests
from pprint import pprint
import collections
import pandas as pd
import time
import pywren
from credentials import access_token

def get_url_groups(csv, num_in_group, max_groups=600, in_done=True):
	groups = []
	tmp = []
	c = 0
	count = 0
	with open('last.txt', 'r+') as last, open(csv, 'r') as f:
		last_done = last.read();
		last_done = last_done.strip('\n')
		print("last_done = [%s]" % last_done)
		for repo in f:
			repo = repo.strip('\n')
			if in_done:
				if last_done == repo:
					in_done = False
				print("Skipping [%s]" % repo)
				continue
			if len(groups) == max_groups:
				print("last %s" % groups[-1][-1])
				last.seek(0)
				last.write(groups[-1][-1])
				last.truncate()
				break
			if c >= num_in_group:
				groups.append(tmp)
				c = 0
				tmp = []
			if c < num_in_group:
				tmp += [repo]
				c += 1
	return groups

def pywren_it(max_executions=600, num_in_group=30):
	start = time.time()
	groups = get_url_groups('repos.csv', num_in_group=num_in_group, max_groups=max_executions)
	print(groups)
	print("%d Groups Running, each with %d repos..." % (len(groups), num_in_group))
	# for group in groups:
	# 	failed, results = get_repo_deets(group)
	# 	print "failed: %s" % failed
	# 	print "results: %s" % results
	wrenexec = pywren.default_executor()
	futures = wrenexec.map(get_repo_deets, groups)
	results = pywren.get_all_results(futures)
	end = time.time()
	failure_count = 0
	succcess_count = 0

	for result in results:
		success = result[2]
		messages = result[1]
		failed = result[0]

		for repo in success:
			print("success: %s" % repo)
			df = pd.DataFrame([repo], columns=['name', 'owner', 'watchers', 'stars', 'forks', 'type', 'issues', 'created_at', 'pushed_at', 'updated_at', 'size', 'open_issues_count', 'description', 'num_languages', 'language_1', 'language_1_size', 'language_2', 'language_2_size', 'language_3', 'language_3_size'])
			with open('github_data.csv', 'a') as f:
				df.to_csv(f, encoding='utf-8', header=f.tell()==0, index=False)
				# print("success %s" % repo)
			succcess_count += 1

		with open('failed.csv', 'a') as f:
			for repo in failed:
				# print("failed %s" % repo)
				f.write(repo+'\n')
				failure_count += 1

		for i, err in enumerate(messages):
			print("repo %s failed with error %s" % (failed[i], err))

	print("Took %f seconds..." %(end - start))
	print("Tried %d repos, %d succeeded and %d failed..." % (max_executions*num_in_group, succcess_count, failure_count))


def get_languages(repo):
	languages = api('repos/%s/languages' % repo)
	stats = collections.Counter(languages)
	return (len(languages), stats.most_common(3))

def get_repo_deets(repos):
	results = []
	failed = []
	messages = []
	for repo in repos:
		# Strip off trailing \n
		repo = repo.strip('\n')
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
				results.append(d)
			else:
				raise Exception('Nonetype returned from api call')
		except Exception as e:
			messages.append("%s failed with error %s" % (repo, e))
			failed.append(repo)
	return failed, messages, results

			
def api(endpoint):
	params = {'access_token': access_token}
	r = requests.get("https://api.github.com/%s" % (endpoint), params=params)
	if r.status_code == 200:
		print("Requests Remaining: %s" % r.headers['X-RateLimit-Remaining'])
		return r.json()
	else:
		print("[%d] <%s>\n%s" % (r.status_code, r.url, r.text))
		return None

if __name__ == '__main__':
	pywren_it(max_executions=250, num_in_group=25)
	# pywren_it(max_executions=600, num_in_group=30)
