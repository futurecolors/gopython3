# coding: utf-8
import datetime
import pytz
from django.test import TestCase
from httpretty import HTTPretty
from .github import Github


class APITestCase(TestCase):
    def setUp(self):
        HTTPretty.reset()
        HTTPretty.enable()

    def tearDown(self):
        HTTPretty.disable()


class TestGithubApi(APITestCase):

    def test_get_most_popular_repo(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/search/repositories',
            '{"items":[{"full_name": "coagulant/requests2", "name": "requests2"},'
                      '{"full_name": "kennethreitz/fake_requests", "name": "fake_requests"}]}',
        )
        self.assertEqual(Github().get_most_popular_repo('fake_requests'), 'kennethreitz/fake_requests')

    def test_get_repo_info(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/coagulant/coveralls-python',
            '{"html_url": "https://github.com/coagulant/coveralls-python", "updated_at": "2013-01-26T19:14:43Z"}',
        )
        self.assertEqual(Github().get_repo('coagulant/coveralls-python'), {
            "html_url": "https://github.com/coagulant/coveralls-python",
            "updated_at": datetime.datetime(2013, 1, 26, 19, 14, 43, tzinfo=pytz.utc)
        })

    def test_get_py3_issues(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/embedly/embedly-python/issues',
            responses=[HTTPretty.Response('[{"state": "open", "title": "WTF?", "html_url": "https://github.com/embedly/embedly-python/issues/1"},'
                                          '{"state": "closed", "title": "Python 3 support", "html_url": "https://github.com/embedly/embedly-python/pull/13"}]'),
                       HTTPretty.Response('[{"state": "open", "title": "Broken", "html_url": "https://github.com/embedly/embedly-python/issues/2"}]')]
        )
        self.assertEqual(Github().get_py3_issues('embedly/embedly-python'), [{
            'state': 'closed',
            'title': 'Python 3 support',
            'html_url': 'https://github.com/embedly/embedly-python/pull/13'
        }])