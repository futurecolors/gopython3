# coding: utf-8
from django.test import TestCase
from django.test.utils import override_settings
from nose.plugins.attrib import attr
from core.models import Job


@override_settings(CELERY_ALWAYS_EAGER=True)
class TestRequirement(TestCase):

    @attr('functional')
    def test_can_be_processed(self):
        requirements = """
            django>1.4,<1.5
            coveralls==0.3
        """
        Job.objects.create_from_requirements(requirements)
