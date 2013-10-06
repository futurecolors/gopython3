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
        # http://developer.github.com/v3/repos/#get
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/coagulant/coveralls-python',
            '{"html_url": "https://github.com/coagulant/coveralls-python", "updated_at": "2013-01-26T19:14:43Z"}',
        )
        self.assertEqual(Github().get_repo('coagulant/coveralls-python'), {
            "html_url": "https://github.com/coagulant/coveralls-python",
            "updated_at": datetime.datetime(2013, 1, 26, 19, 14, 43, tzinfo=pytz.utc)
        })
