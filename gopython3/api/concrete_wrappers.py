from django.conf import settings
import requests

from . import abstract_wrappers


PYTHON_3_KEYWORDS = (
    'Python 3',
    'python3',
    'py 3',
    'py3',
    'py 3k'
    'py3k'
    'python 3000',
    'python3000',
)


class PyPIWrapper(abstract_wrappers.AbstractJsonApiWrapper):
    base_url = 'http://pypi.python.org/pypi'

    def package_info(self, name, version=None):
        self.hammock = self.hammock(name)
        if version:
            self.hammock = self.hammock(version)
        self.hammock = self.hammock.json
        return 'GET', {}

    def get_short_info(self, name, version=None):
        name = self.get_correct_name(name)
        data = self.ask_about_package_info(name=name, version=version)
        return {
            'last_release_date': data['urls'][0]['upload_time'],
            'python3_supported_versions': list(self.get_py3_supported_versions(data)),
            'url': data['info']['package_url'],
            'name': name,
            'version': data['info']['version']
        }

    def get_py3_supported_versions(self, data):
        language_classifiers = data['info']['classifiers']
        python_info = filter(lambda c: c.startswith('Programming Language') and 'Python' in c, language_classifiers)
        py3_versions = filter(lambda v: v[0] == '3', [v.split('::')[-1].strip() for v in python_info])
        return py3_versions

    def get_correct_name(self, name):
        response = requests.get('http://pypi.python.org/simple/%s/' % name)
        return response.url.split('/')[-2]


class GithubWrapper(abstract_wrappers.AbstractJsonApiWrapperWithAuth):
    base_url = 'https://api.github.com'

    def get_credentials(self):
        return {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
        }

    def repo_info(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo)
        return 'GET', {}

    def repo_forks(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo).forks
        print(self.hammock)
        return 'GET', {}

    def repo_branches(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo).branches
        print('branches', self.hammock)
        return 'GET', {}

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