from django.conf import settings

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

    def get_credentials(self):
        return {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
        }

    def get_short_info(self, owner, repo):
        data = self.ask_about_repo_info(owner=owner, repo=repo)
        return {
            'url': data['url'],
            'updated_at': data['updated_at'],
            'py3_fork': self.get_py3_fork_info(owner, repo),
            'py3_issue': self.get_py3_issue_info(owner, repo),
            'services_info': self.get_services_info(owner, repo)
        }

    def get_py3_fork_info(self, owner, repo):
        fields_to_lookup = ('full_name', 'description')
        forks = self.ask_about_repo_forks(owner=owner, repo=repo)
        py3_forks = []
        for fork in forks:
            search_data = [fork[field].lower() for field in fields_to_lookup]
            if self._has_py3_tracks(search_data):
                py3_forks.append(fork)
            else:
                branches_info = self.ask_about_repo_branches(owner=fork['owner']['login'], repo=fork['name'])
                if self._has_py3_tracks([b['name'] for b in branches_info]):
                    py3_forks.append(fork)

        return {} if not py3_forks else {
            'status': 'fork',
            'url': py3_forks[0]['url']
        }

    def get_py3_issue_info(self, owner, repo):
        return ''

    def get_services_info(self, owner, repo):
        return ''

    def _has_py3_tracks(self, data):
        return any([keyword.lower() in ''.join(data) for keyword in PYTHON_3_KEYWORDS])


class GithubSearchWrapper(abstract_wrappers.AbstractJsonApiWrapperWithAuth):
    base_url = 'https://api.github.com'
    search_page_size = 20

    def popular_repos(self, repo):
        extra_request_data = {
            'params': {
                'q': '%s+in:name+language:python' % repo,
                'sort': 'stars',
                'per_page': self.search_page_size
            }
        }
        self.hammock = self.hammock.search.repositories
        return 'GET', extra_request_data

    def get_most_popular_repo(self, repo):
        """ Return most popular owner/repo pair for given repo"""
        repos = self.ask_about_popular_repos(repo=repo)
        if 'items' in repos:
            repos_names_and_owners = [(r['name'], r['owner']['login']) for r in repos['items']]
            repos_with_same_name = list(filter(lambda n: repo.lower() == n[0].lower(), repos_names_and_owners))
            if repos_with_same_name:
                return repos_with_same_name[0]

    def get_common_request_kwargs(self):
        search_headers = {'Accept': 'application/vnd.github.preview'}
        kwargs = super(GithubSearchWrapper, self).get_common_request_kwargs()
        if 'headers' in kwargs:
            kwargs['headers'].update(search_headers)
        else:
            kwargs['headers'] = search_headers
        return kwargs
