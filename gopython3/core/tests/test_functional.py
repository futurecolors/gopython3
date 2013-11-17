# coding: utf-8
import logging
from django.test import TestCase
from django.test.utils import override_settings
import pytest
from core.models import Job


logger = logging.getLogger('core')


@override_settings(CELERY_ALWAYS_EAGER=True,
                   CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
class TestRequirement(TestCase):

    def setUp(self):
        logger.setLevel(logging.DEBUG)

    def tearDown(self):
        logger.setLevel(logging.ERROR)

    @pytest.mark.functional
    def test_can_be_processed(self):

        requirements = """
            not_on_pypi
            django>1.4,<1.5
            django-compressor==1.3
        """
        Job.objects.create_from_requirements(requirements).start()


@pytest.mark.functional
class TestHttp(TestCase):

    def test_index(self):
        response = self.client.get('/404/')
        assert response.status_code == 404
