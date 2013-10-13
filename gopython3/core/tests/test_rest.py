# coding: utf-8
from rest_framework.test import APITestCase
from core.factories import JobFactory


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
