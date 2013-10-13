# coding: utf-8
from rest_framework.test import APITestCase
from core.factories import JobFactory, SpecFactory


class TestApi(APITestCase):

    def test_jobs_list(self):
        job = JobFactory()
        response = self.client.get('/api/v1/jobs/', format='json')
        self.assertDictEqual(response.data, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'id': 1,
                'url': 'http://testserver/api/v1/jobs/1/',
                'status': 'pending',
                'created_at': job.created_at,
                'updated_at': job.updated_at,
                'started_at': None,
                'finished_at': None
            }]
        })

    def test_job_detail(self):
        # TODO: SpecFactory(line='django_model_utils==1.5.0')
        job = JobFactory(specs=[SpecFactory(package__name='django-model-utils', version='1.5.0'),
                                SpecFactory(package__name='jsonfield', version='0.9.19')],
                         status='running')
        response = self.client.get('/api/v1/jobs/1/', format='json')
        self.assertDictEqual(response.data, {
            "id": 1,
            "url": "http://testserver/api/v1/jobs/1/",
            "status": "running",
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
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "started_at": None,
            "finished_at": None
        })
