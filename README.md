
# Github Data Analysis

Sean Smith <swsmith@bu.edu> [sean-smith](https://github.com/sean-smith)

Ann Ming Samborski <asambors@bu.edu> [asamborski](https://github.com/asamborski)

### Data Source

We are going to scrape github.com for publically acessible github repositories and collect the following information:

* stars
* forks
* followers
* owner_id
* org_name
* primary_language
* secondary_language
* lines_of_code
* num_contributors
* first_commit
* num_pull_requests
* speaking_language
* num_commits
* commit_times
* loc_per_comit
* type_of_computer (.DS_Store ftw)

With this data we want to answer a bunch of questions.

1. What are the most popular coding languages? How has this changed over time? 
2. Given commit times, can we predict number of stars? 
3. Does lines of code correlate with number of stars?
4. Do number of contributors correlate with number of stars?
5. What are the most popular repositories to contribute to?
6. How does contributions vary by country? By time zone?
7. Does number of commits correlate with lines of code?
8. What repository has the most number of commits?
9. Do organizations have less or more contributors? Lines of code?
10. Do Chinese speaking people use github? Do they use it in China? (see [great cannon](https://citizenlab.org/2015/04/chinas-great-cannon/) for context)
