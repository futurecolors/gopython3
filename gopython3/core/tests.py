import warnings
from unittest.mock import patch
from collections import namedtuple

from django.test.utils import override_settings
from django.test import TestCase
from core.factories import SpecFactory

from .models import Job, Package, Spec, JobSpec


def fake_distributions(*distributions):
    Distribution = namedtuple('Distribution', ['name', 'version'])
    result = []
    for dist in distributions:
        name, version = dist.split('==')
        result.append(Distribution(name, version))
    return result


@override_settings(CELERY_ALWAYS_EAGER=True)
class JobTest(TestCase):

    @patch('api2.pypi.locate', side_effect=fake_distributions(
           'Django==1.4.8', 'django-geoip==0.3', 'coverage==3.7', 'coveralls==0.3'))
    def test_can_be_created_from_requirements_txt(self, locate_mock):
        reqs_txt = """
            -r some_missing_file
            django>=1.4,<1.5
            Django-Geoip==0.3
            # tests below
            coverage
            coveralls>0.2
            # TODO: VCS
        """
        with warnings.catch_warnings():
            # We're ignoring -r not being parsed
            # "Recursive requirements not supported. Skipping."
            warnings.simplefilter("ignore", category=UserWarning)
            job = Job.objects.create_from_requirements(reqs_txt)

        assert job.requirements == reqs_txt
        self.assertQuerysetEqual(Package.objects.all(),
             ['Django (django)', 'django-geoip (django_geoip)', 'coverage (coverage)', 'coveralls (coveralls)'],
             transform=str, ordered=False)
        self.assertQuerysetEqual(Spec.objects.all(),
             ['Django==1.4.8', 'django-geoip==0.3', 'coverage==3.7', 'coveralls==0.3'],
             transform=str, ordered=False)
        self.assertQuerysetEqual(JobSpec.objects.all(),
             ['Job 1 [pending] Django==1.4.8', 'Job 1 [pending] django-geoip==0.3',
              'Job 1 [pending] coverage==3.7', 'Job 1 [pending] coveralls==0.3'],
             transform=str, ordered=False)

    @patch('api2.pypi.locate', side_effect=fake_distributions('lettuce==0.2.19'))
    def test_does_not_create_duplicate_specs(self, locate_mock):
        spec = SpecFactory(version='0.2.19', package__name='lettuce', package__slug='lettuce')
        job = Job.objects.create_from_requirements('lettuce==0.2.19')

        assert Spec.objects.count() == 1
        assert Package.objects.count() == 1
        assert job.specs.all().first().version == spec.version
        assert job.specs.all().first().package.name == spec.package.name
