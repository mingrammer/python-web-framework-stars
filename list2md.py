from datetime import datetime
import json
import requests


head = '''# Top Python Web Frameworks
A list of popular github projects related to Python web framework (ranked by stars automatically)
Please update **list.txt** (via Pull Request)

| Project Name | Stars | Forks | Open Issues | Description | Last Commit |
| ------------ | ----- | ----- | ----------- | ----------- | ----------- |
'''
tail = '\n*Last Automatic Update: {}*'

warning = "⚠️ No longer maintained ⚠️  "

deprecated_repos = list()
repos = list()


def main():
    access_token = get_access_token()

    with open('list.txt', 'r') as f:
        for url in f.readlines():
            url = url.strip()
            if url.startswith('https://github.com/'):
                repo_api = 'https://api.github.com/repos/{}?access_token={}'.format(url[19:], access_token)
                print(repo_api)

                r = requests.get(repo_api)
                if r.status_code != 200:
                    raise ValueError('Can not retrieve from {}'.format(url))
                repo = json.loads(r.content)
                
                commit_api = 'https://api.github.com/repos/{}/commits/{}?access_token={}'.format(url[19:], repo['default_branch'], access_token)
                print(repo_api)

                r = requests.get(commit_api)
                if r.status_code != 200:
                    raise ValueError('Can not retrieve from {}'.format(url))
                commit = json.loads(r.content)
                
                repo['last_commit_date'] = commit['commit']['committer']['date']
                repos.append(repo)
        
        repos.sort(key=lambda r: r['stargazers_count'], reverse=True)
        save_ranking(repos)


def get_access_token():
    with open('access_token.txt', 'r') as f:
        return f.read().strip()


def save_ranking(repos):
    with open('README.md', 'w') as f:
        f.write(head)
        for repo in repos:
            if is_deprecated(repo['url']):
                repo['description'] = warning + repo['description']
            f.write('| [{}]({}) | {} | {} | {} | {} | {} |\n'.format(repo['name'],
                                                                     repo['url'],
                                                                     repo['stargazers_count'],
                                                                     repo['forks_count'],
                                                                     repo['open_issues_count'],
                                                                     repo['description'],
                                                                     datetime.strptime(repo['last_commit_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')))
        f.write(tail.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S%Z')))


def is_deprecated(repo_url):
    return repo_url in deprecated_repos


if __name__ == '__main__':
    main()