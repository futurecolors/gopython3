# coding: utf-8
from django.conf import settings
from hammock import Hammock


class HammockAPI(object):
    base_url = None

    def __init__(self, *args, **kwargs):
        self.api = Hammock(self.base_url, params=self.params(), headers=self.headers(), proxies={})

    def params(self):
        return {}

    def headers(self):
        return {}


class Github(HammockAPI):
    base_url = 'https://api.github.com'

    def params(self):
        return {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
        }

    def headers(self):
        return {
            'Accept': 'application/vnd.github.preview'
        }

    def get_most_popular_repo(self, package_name, language='python'):
        """ Most popular owner/repo fullname for given package name
            Returns None if no matches found.
        """

        # http://developer.github.com/v3/search/#repository-search-example
        repos = self.api.search.repositories.GET(params={
            'q': '%s+in:name+language:%s' % (package_name, language),
            'per_page': 10,
        }).json()

        for repo in repos.get('items', []):
            # TODO: maybe more intelligent name guess?
            if repo['name'].lower() == package_name:
                return repo['full_name']

