from . import abstract_wrappers
from django.conf import settings


class PyPIWrapper(abstract_wrappers.AbstractJsonApiWrapper):
    base_url = 'http://pypi.python.org/pypi'

    def package_info(self, name, version=None):
        self.hammock = self.hammock(name)
        if version:
            self.hammock = self.hammock(version)
        self.hammock = self.hammock.json
        return 'GET', {}


class GithubWrapper(abstract_wrappers.AbstractJsonApiWrapperWithAuth):
    base_url = 'https://api.github.com'

    def get_credentials(self):
        return {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
        }

    def repository_info(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo)
        return 'GET', {}
