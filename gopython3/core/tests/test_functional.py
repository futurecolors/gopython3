# coding: utf-8
import logging
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from nose.plugins.attrib import attr
from core.models import Job


logger = logging.getLogger('core')


@override_settings(CELERY_ALWAYS_EAGER=True)
class TestRequirement(TestCase):

    def setUp(self):
        logger.setLevel(logging.DEBUG)

    def tearDown(self):
        logger.setLevel(logging.ERROR)

    @attr('functional')
    def test_can_be_processed(self):

        requirements = """
            django>1.4,<1.5
            coveralls==0.3
        """
        Job.objects.create_from_requirements(requirements)


class TestHttp(TestCase):

    @attr('functional')
    def test_index(self):
        """ Need imporvement, does not catch anything yet
            FIXME: gopython3-6, need admin tests too
        """
        response = self.client.get('/')
        self.assertTrue('Go Python 3!' in str(response.content))
        self.assertEqual(response.status_code, 200)
