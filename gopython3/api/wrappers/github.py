from urllib.parse import urlparse

from django.conf import settings
from django.utils.dateparse import parse_datetime

from api import abstract_wrappers
from api.wrappers import PYTHON_3_KEYWORDS


class GithubWrapper(abstract_wrappers.AbstractJsonApiWrapperWithAuth):
    base_url = 'https://api.github.com'

    def repo_info(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo)
        return 'GET', {}

    def repo_forks(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo).forks
        return 'GET', {}

    def repo_branches(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo).branches
        return 'GET', {}

    def repo_pull_requests(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo).pulls
        return 'GET', {}

    def repo_issues(self, owner, repo, state=None):
        self.hammock = self.hammock.repos(owner, repo).issues
        if state:
            additional_data = {'params': {'state': state}}
        else:
            additional_data = {}
        return 'GET', additional_data

    def rate_limit(self):
        self.hammock = self.hammock.rate_limit
        return 'GET', {}

    def get_credentials(self):
        return {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
        }

    def get_short_info(self, owner, repo):
        data = self.ask_about_repo_info(owner=owner, repo=repo)
        return {
            'url': data['html_url'],
            'updated_at': parse_datetime(data['updated_at']),
        }

    def get_py3_fork_info(self, owner, repo, check_branches=False):
        fields_to_lookup = ('full_name', 'description')
        forks = self.ask_about_repo_forks(owner=owner, repo=repo)
        py3_forks = []
        for fork in forks:
            search_data = [fork[field].lower() for field in fields_to_lookup]
            if self._has_py3_tracks(search_data):
                py3_forks.append(fork)
            elif check_branches:
                branches_info = self.ask_about_repo_branches(owner=fork['owner']['login'], repo=fork['name'])
                if self._has_py3_tracks([b['name'] for b in branches_info]):
                    py3_forks.append(fork)

        return {} if not py3_forks else {
            'status': 'fork',
            'url': py3_forks[0]['url']
        }

    def get_py3_issues_info(self, owner, repo):
        issues = self.ask_about_repo_issues(owner=owner, repo=repo, state='open') or []
        closed_issues = self.ask_about_repo_issues(owner=owner, repo=repo, state='closed') or []
        issues += closed_issues
        if issues:
            issues_data = [{'number': i['number'], 'data': ''.join([i['title'] or '', i['body'] or ''])} for i in issues]
            filtered_issues_numbers = [i['number'] for i in filter(lambda i: self._has_py3_tracks([i['data']]), issues_data)]
            if filtered_issues_numbers:
                py3_issues = filter(lambda i: i['number'] in filtered_issues_numbers, issues)
                return [{
                    'state': i['state'],
                    'title': i['title'],
                    'url': i['html_url']
                } for i in py3_issues]
        else:
            return []

    def get_py3_pull_requests(self, owner, repo):
        pulls = self.ask_about_repo_pull_requests(owner=owner, repo=repo)
        fields_to_lookup = ('title', 'body')
        py3_pulls = []
        for pull in pulls:
            search_data = [pull[field].lower() for field in fields_to_lookup]
            if self._has_py3_tracks(search_data):
                py3_pulls.append({
                    'url': pull['html_url'],
                    'issue_url': pull['html_url'],
                    'title': pull['title'],
                    'body': pull['body'],
                    'state': pull['state'],
                })
        return py3_pulls

    def _has_py3_tracks(self, data):
        return any([keyword.lower() in ''.join(data).lower() for keyword in PYTHON_3_KEYWORDS])

    def parse_github_url(self, url):
        """ Returns owner/repo dict for github repo url (like https://github.com/futurecolors/djangodash2013)."""
        parsed_url = urlparse(url)
        host, path = parsed_url.hostname, parsed_url.path
        if host == 'github.com':
            splitted = path.strip('/').split('/')
            if len(splitted) == 2:
                return {
                    'owner': splitted[0],
                    'repo': splitted[1],
                }
        return None


class GithubSearchWrapper(abstract_wrappers.AbstractJsonApiWrapperWithAuth):
    base_url = 'https://api.github.com'
    search_page_size = 20

    def popular_repos(self, repo=None, extra_params=None):
        if not (repo or extra_params):
            raise AttributeError('Specify repo or extra_data')
        extra_request_data = {
            'params': {
                'q': '%s+in:name+language:python' % repo,
                'per_page': self.search_page_size
            }
        }
        if extra_params:
            extra_request_data['params'].update(extra_params)
        self.hammock = self.hammock.search.repositories
        return 'GET', extra_request_data

    def get_most_popular_repo(self, repo):
        """ Return most popular owner/repo pair for given repo"""
        repos = self.ask_about_popular_repos(repo=repo)
        if 'items' in repos:
            repos_names_and_owners = [(r['name'], r['owner']['login']) for r in repos['items']]
            if repos_names_and_owners:
                return repos_names_and_owners[0]

    def get_common_request_kwargs(self):
        search_headers = {'Accept': 'application/vnd.github.preview'}
        kwargs = super(GithubSearchWrapper, self).get_common_request_kwargs()
        if 'headers' in kwargs:
            kwargs['headers'].update(search_headers)
        else:
            kwargs['headers'] = search_headers
        return kwargs
