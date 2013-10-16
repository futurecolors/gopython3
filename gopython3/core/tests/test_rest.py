# coding: utf-8
import datetime
from django.utils.timezone import now, pytz
from rest_framework.test import APITestCase
from core.factories import JobFactory, SpecFactory


class TestApi(APITestCase):
    maxDiff = None

    def setUp(self):
        self.job = JobFactory(specs=['django-model-utils==1.5.0', 'jsonfield==0.9.19'])

    def test_api_root(self):
        response = self.client.get('/api/v1/')
        assert 'jobs' in response.data
        assert 'packages' in response.data

    def test_post_job(self):
        response = self.client.post('/api/v1/jobs/', {'requirements': 'foo\nbar>1.2'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], 'http://testserver/api/v1/jobs/2/')

    def test_jobs_list(self):
        response = self.client.get('/api/v1/jobs/', format='json')
        self.assertDictEqual(response.data, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                            'id': 1,
                            'url': 'http://testserver/api/v1/jobs/1/',
                            'status': 'pending',
                            'created_at': self.job.created_at,
                            'updated_at': self.job.updated_at,
                            'started_at': None,
                            'finished_at': None
                        }]
        })

    def test_job_detail(self):
        response = self.client.get('/api/v1/jobs/1/', format='json')
        self.assertDictEqual(response.data, {
            "id": 1,
            "url": "http://testserver/api/v1/jobs/1/",
            "status": "pending",
            "packages": [{
                             "id": "django_model_utils/1.5.0",
                             "url": "http://testserver/api/v1/packages/django_model_utils/1.5.0/",
                             "name": "django-model-utils",
                             "version": "1.5.0"
                         }, {
                             "id": "jsonfield/0.9.19",
                             "url": "http://testserver/api/v1/packages/jsonfield/0.9.19/",
                             "name": "jsonfield",
                             "version": "0.9.19"
                         }],
            "created_at": self.job.created_at,
            "updated_at": self.job.updated_at,
            "started_at": None,
            "finished_at": None
        })

    def test_spec_detail(self):
        spec =  SpecFactory(package__name='django-compressor',
                            version='1.3',
                            status='completed',
                            package__repo_url='https://github.com/jezdez/django_compressor',
                            package__repo_last_commit_date=datetime.datetime(2013, 9, 22, 1, 56, 12, tzinfo=pytz.utc),
                            package__issue_url='https://github.com/jezdez/django_compressor/issues/360',
                            package__issue_status='closed',
                            package__ci_url='https://travis-ci.org/jezdez/django_compressor',
                            package__ci_status='passing',
                            release_date=datetime.datetime(2013, 9, 22, 1, 56, 12, tzinfo=pytz.utc),
                            python_versions=['3.3'],
                            package__comment_count=1,
                            package__comment_most_voted='Enlarge your python!'
        )
        package = spec.package

        response = self.client.get('/api/v1/packages/django_compressor/1.3/', format='json')
        self.assertDictEqual(response.data, {
             "id": "django_compressor/1.3",
             "name": "django-compressor",
             "version": "1.3",
             "status": "completed",
             "created_at": spec.created_at,
             "updated_at": spec.updated_at,
             "pypi": {
                 "current": {
                     "url": "https://pypi.python.org/pypi/django_compressor/1.3",
                     "version": "1.3",
                     "python3": ["3.3"],
                     "release_date": spec.release_date
                 },
                 "latest": {
                     "url": "https://pypi.python.org/pypi/django_compressor/1.3",
                     "version": "1.3",
                     "python3": ["3.3"],
                     "release_date": spec.release_date
                 }
             },
             "repo": {
                 "url": "https://github.com/jezdez/django_compressor",
                 "last_commit_date": package.repo_last_commit_date,
             },
             "issues": [{
                 "url": "https://github.com/jezdez/django_compressor/issues/360",
                 "status": "closed"
             }],
             "forks": [],
             "ci": {
                 "url": "https://travis-ci.org/jezdez/django_compressor",
                 "status": "passing"
             },
             'url': 'http://testserver/api/v1/packages/django_compressor/1.3/'
        })


