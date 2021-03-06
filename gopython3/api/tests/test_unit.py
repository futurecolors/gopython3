# coding: utf-8
import datetime
import pytz
from django.test import TestCase
from httpretty import HTTPretty
from api.pypi import PyPI
from api.travis import TravisCI
from api.github import Github


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
        assert Github().get_most_popular_repo('Fake_Requests') == 'kennethreitz/fake_requests'

    def test_get_repo_info(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/coagulant/coveralls-python',
            '{"html_url": "https://github.com/coagulant/coveralls-python", "updated_at": "2013-01-26T19:14:43Z"}',
        )
        assert Github().get_repo('coagulant/coveralls-python') == {
            "html_url": "https://github.com/coagulant/coveralls-python",
            "updated_at": datetime.datetime(2013, 1, 26, 19, 14, 43, tzinfo=pytz.utc)
        }

    def test_crawl_py3_issues(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/embedly/embedly-python/issues',
            responses=[HTTPretty.Response('[{"state": "open", "title": "WTF?", "html_url": "https://github.com/embedly/embedly-python/issues/1"},'
                                          '{"state": "closed", "title": "Python 3 support", "html_url": "https://github.com/embedly/embedly-python/pull/13"}]'),
                       HTTPretty.Response('[{"state": "open", "title": "Broken", "html_url": "https://github.com/embedly/embedly-python/issues/2"}]')]
        )
        assert Github().get_py3_issues('embedly/embedly-python', search=False) == [{
            'state': 'closed',
            'title': 'Python 3 support',
            'html_url': 'https://github.com/embedly/embedly-python/pull/13'
        }]
        assert HTTPretty.last_request.querystring['state'][0] == 'closed'

    def test_get_py3_pull_requests(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/django/django/pulls',
            responses=[HTTPretty.Response('[{"html_url": "https://github.com/django/django/pull/1", "title": "testing python requests 3", "state": "open"},'
                                          ' {"html_url": "https://github.com/django/django/pull/2", "title": "please support Python 3", "state": "closed"}]'),
                       HTTPretty.Response('[{"state": "open", "title": "Broken", "html_url": "https://github.com/django/django/pull/3"}]')]
        )
        assert Github().get_py3_pulls('django/django') == [{
            'state': 'closed',
            'title': 'please support Python 3',
            'html_url': 'https://github.com/django/django/pull/2'
        }]
        assert HTTPretty.last_request.querystring['state'][0] == 'closed'

    def test_get_py3_forks(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/nick/progressbar/forks',
            '[{"html_url": "https://github.com/coagulant/progressbar-python3", "name": "progressbar-python3"},'
             '{"html_url": "https://github.com/mick/progressbar", "name": "progressbar"}]',
        )
        assert Github().get_py3_forks('nick/progressbar') == [{
            'name': 'progressbar-python3',
            'html_url': 'https://github.com/coagulant/progressbar-python3'
        }]

    def test_get_py3_forks_branches(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/embedly/embedly-python/forks',
            '[{"html_url": "https://github.com/coagulant/embedly-python", "name": "embedly-python", "full_name": "coagulant/embedly-python"}]',
        )
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.github.com/repos/coagulant/embedly-python/branches',
            '[{"name": "master"}, {"name": "py3k"}]',
        )
        assert Github().get_py3_forks('embedly/embedly-python', True) == [{
            'name': 'embedly-python',
            'html_url': 'https://github.com/coagulant/embedly-python'
        }]


class TestTravisApi(APITestCase):

    def test_get_build_status(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.travis-ci.org/repos/coagulant/cleanweb',
            '{"repo":{"slug": "coagulant/cleanweb", "last_build_state": "passed"}}'
        )
        assert TravisCI().get_build_status('coagulant/cleanweb') == {
            'html_url': 'https://travis-ci.org/coagulant/cleanweb',
            'last_build_state': 'passed',
        }

    def test_get_build_status_partial(self):
        HTTPretty.register_uri(HTTPretty.GET,
            'https://api.travis-ci.org/repos/coxmediagroup/django-admin-tools',
            '{"repo":{"slug": "coxmediagroup/django-admin-tools", "last_build_state": ""}}'
        )
        assert TravisCI().get_build_status('coxmediagroup/django-admin-tools') == {
            'html_url': 'https://travis-ci.org/coxmediagroup/django-admin-tools',
            'last_build_state': 'unknown',
        }


class TestPypiApi(APITestCase):

    def test_get_info_without_version(self):
        json_string = """{"info":{
        "name": "Django",
        "home_page": "http://www.djangoproject.com/",
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

        assert PyPI().get_info('Django') == {
            'py3_versions': ['3', '3.2', '3.3'],
            'last_release_date': datetime.datetime(2013, 9, 15, 6, 30, 37, tzinfo=pytz.utc),
            'name': 'Django',
            'url': 'http://www.djangoproject.com/'
        }

    def test_get_info_with_version(self):
        json_string = """{"info":{
        "name": "Django",
        "home_page": "http://www.djangoproject.com/",
        "classifiers": [
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.4",
            "Programming Language :: Python :: 2.5",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7"]
        }, "urls": [{"upload_time": "2013-02-19T20:32:04"}]}"""
        HTTPretty.register_uri(HTTPretty.GET,
            "http://pypi.python.org/pypi/Django/1.3.6/json", json_string
        )

        assert PyPI().get_info(name='Django', version='1.3.6') == {
            'py3_versions': [],
            'last_release_date': datetime.datetime(2013, 2, 19, 20, 32, 4, tzinfo=pytz.utc),
            'name': 'Django',
            'url': 'http://www.djangoproject.com/'
        }

    def test_incomplete_info(self):
        json_string = """{"info":{
        "name": "printtree",
        "home_page": "UNKNOWN",
        "classifiers": []
        }, "urls": []}"""
        HTTPretty.register_uri(HTTPretty.GET,
            "http://pypi.python.org/pypi/printtree/1.0.10/json", json_string
        )

        assert PyPI().get_info(name='printtree', version='1.0.10') == {
            'py3_versions': [],
            'last_release_date': None,
            'name': 'printtree',
            'url': None
        }
