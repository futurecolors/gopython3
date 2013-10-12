# coding: utf-8
from django.core.cache import cache
from django.test import TestCase
from nose.plugins.attrib import attr
from api.github import Github


@attr('functional')
class GithubRealTest(TestCase):

    def setUp(self):
        self.gh = Github()

    @attr('functional')
    def test_github_api_with_real_repos(self):
        repos = cache.get('top_popular_repos')
        if not repos:
            # Get 100 most popular repos
            repos = self.gh.api.search.repositories.GET(params={
                'q': 'language:python',
                'per_page': 100,
                'sort': 'stars',
            }).json()
            cache.set('top_popular_repos', repos)

        for i, repo in enumerate(repos['items']):
            full_name = repo['full_name']
            print(i,
                  full_name,
                  'forks: %s' % len(self.gh.get_py3_forks(full_name)),
                  'issues: %s' % len(self.gh.get_py3_issues(full_name) or self.gh.get_py3_pulls(full_name))
            )
