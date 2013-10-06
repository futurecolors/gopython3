# coding: utf-8
import datetime
import pytz
from django.test import TestCase
from httpretty import HTTPretty
from api2.pypi import PyPI
from .travis import Travis
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

    def test_get_py3_forks(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/nick/progressbar/forks',
            '[{"html_url": "https://github.com/coagulant/progressbar-python3", "name": "progressbar-python3"},'
             '{"html_url": "https://github.com/mick/progressbar", "name": "progressbar"}]',
        )
        self.assertEqual(Github().get_py3_forks('nick/progressbar'), [{
            'name': 'progressbar-python3',
            'html_url': 'https://github.com/coagulant/progressbar-python3'
        }])


class TestTravisApi(APITestCase):

    def test_get_build_status(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.travis-ci.org/repos/coagulant/cleanweb',
            '{"repo":{"slug": "coagulant/cleanweb", "last_build_state": "passed"}}'
        )
        self.assertEqual(Travis().get_build_status('coagulant/cleanweb'), {
            'html_url': 'https://travis-ci.org/coagulant/cleanweb',
            'last_build_state': 'passed',
        })


class TestPypiApi(APITestCase):

    def test_get_info(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'http://pypi.python.org/simple/django/', status=302,
            Location='http://pypi.python.org/simple/Django/'
        )
        HTTPretty.register_uri(HTTPretty.GET,
           'http://pypi.python.org/simple/Django/',
           body="it works!")

        json_string = """{"info":{
        "classifiers": [
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3"]
        }, "urls": [{"upload_time": "2013-09-15T06:30:37"}]}"""
        HTTPretty.register_uri(HTTPretty.GET,
            "http://pypi.python.org/pypi/Django/json", json_string
        )

        self.assertEqual(PyPI().get_info('django'), {
            'py3_versions': ['3', '3.2', '3.3'],
            'name': 'Django',
            'last_release_date': datetime.datetime(2013, 9, 15, 6, 30, 37, tzinfo=pytz.utc),
        })
