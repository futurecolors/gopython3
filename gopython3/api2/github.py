# coding: utf-8
from itertools import chain
from urllib.parse import urlparse
import logging
import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime
from .base import HammockAPI, is_py3_topic


logger = logging.getLogger(__name__)


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

    @classmethod
    def parse_url(cls, url):
        """ Returns owner/repo part for github repo url.
            None if not a github url

        >>> Github.parse_url('https://github.com/futurecolors/djangodash2013')
        'futurecolors/djangodash2013'
        >>> Github.parse_url('https://github.com/futurecolors/django-geoip/')
        'futurecolors/django-geoip'

        """
        parsed_url = urlparse(url)
        host, path = parsed_url.hostname, parsed_url.path
        if host == 'github.com':
            path = path.strip('/')
            if path.count('/') == 1:
                return path
        return None

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

    def get_py3_issues(self, full_name, search=True):
        """ Issues with python 3 in title
            Can be obtained via legacy but working query
            and by manually querying all issue pages (multiple queries)
        """
        if search:
            return self._search_py3_issues(full_name)
        else:
            # pending deprecation?
            return self._crawl_py3_issues(full_name)

    def _search_py3_issues(self, full_name):
        """ Search for issues with python+3 in title

            Note: returns pulls as well, legacy method
            TODO: undocumented search exists curl -ni "https://api.github.com/search/issues?q=chrome+repo:twbs/bootstrap"

            JSON http://developer.github.com/v3/issues/#list-issues-for-a-repository
        """
        open_issues = self.api.legacy.issues.search(full_name).open('python+3').GET().json()
        closed_issues = self.api.legacy.issues.search(full_name).closed('python+3').GET().json()
        return [{'state': issue['state'], 'title': issue['title'], 'html_url': issue['html_url']}
                for issue in chain(open_issues['issues'], closed_issues['issues'])]

    def _crawl_py3_issues(self, full_name):
        """ Issues with py3 keywords in title

            JSON http://developer.github.com/v3/issues/#list-issues-for-a-repository
        """
        # TODO: maybe parse more than 2 pages
        open_issues = self.api.repos(full_name).issues.GET()
        if open_issues.status_code == requests.codes.gone:
            # Issue tracker is disabled for this repo
            return []
        closed_issues = self.api.repos(full_name).issues.GET(params={'state': 'closed'})
        return [{'state': issue['state'], 'title': issue['title'], 'html_url': issue['html_url']}
                for issue in chain(open_issues.json(), closed_issues.json()) if is_py3_topic(issue['title'])]

    def get_py3_pulls(self, full_name):
        """ Pull requests with py3 keywords in name

            Pull requests are also issues if issue tracker is not disabled,
            in most cases fetching get_py3_issues is enough to cover both issues and PRs.

            JSON http://developer.github.com/v3/pulls/#list-pull-requests
        """
        open_prs = self.api.repos(full_name).pulls.GET()
        closed_prs = self.api.repos(full_name).pulls.GET(params={'state': 'closed'})

        return [{'state': pull['state'], 'title': pull['title'], 'html_url': pull['html_url']}
                for pull in chain(open_prs.json(), closed_prs.json()) if is_py3_topic(pull['title'])]

    def get_py3_forks(self, full_name, check_branches=False):
        """ Forks with py3 keywords in name

            Optional branches arg will search branch names for python 3 name
            (query per fork, so takes plenty of time)

            TODO: support undocumented network_meta json
                  https://github.com/flavioamieiro/nose-ipdb/network_meta
                  Currently it's almost useless, people rarely rename their forks.

            JSON http://developer.github.com/v3/repos/forks/#list-forks
                 http://developer.github.com/v3/repos/#list-branches
        """
        def get_branch_names(fork):
            if not check_branches:
                return ['']
            branches_info = self.api.repos(fork['full_name']).branches.GET().json()
            return [branch['name'] for branch in branches_info]

        forks = self.api.repos(full_name).forks.GET().json()
        return [{'html_url': fork['html_url'], 'name': fork['name']}
                for fork in forks if is_py3_topic(fork['name'], *get_branch_names(fork))]
