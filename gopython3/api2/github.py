# coding: utf-8
from itertools import chain
from django.conf import settings
from django.utils.dateparse import parse_datetime
from hammock import Hammock


def is_py3_topic(*args):
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
    target_string = ''.join(args).lower()
    return any([keyword.lower() in target_string for keyword in PYTHON_3_KEYWORDS])


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

            JSON: http://developer.github.com/v3/search/#repository-search-example
        """
        repos = self.api.search.repositories.GET(params={
            'q': '%s+in:name+language:%s' % (package_name, language),
            'per_page': 10,
        }).json()

        for repo in repos.get('items', []):
            # TODO: maybe more intelligent name guess?
            if repo['name'].lower() == package_name:
                return repo['full_name']

    def get_repo(self, full_name):
        """ Repo info

            JSON http://developer.github.com/v3/repos/#get
        """
        repo = self.api.repos(full_name).GET().json()
        return {
            'html_url': repo['html_url'],
            'updated_at': parse_datetime(repo['updated_at']),
        }

    def get_py3_issues(self, full_name):
        """ Issues with py3 keywords in title
            Returns None if no matches found.

            JSON http://developer.github.com/v3/issues/#list-issues-for-a-repository
        """
        # TODO: maybe parse more than 2 pages
        open_issues = self.api.repos(full_name).issues.GET().json()
        closed_issues = self.api.repos(full_name).issues.GET(params={'state': 'closed'}).json()
        return [{'state': issue['state'], 'title': issue['title'], 'html_url': issue['html_url']}
                for issue in chain(open_issues, closed_issues) if is_py3_topic(issue['title'])]
