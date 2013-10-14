# coding: utf-8
from unittest.mock import patch
from django.utils import timezone

import warnings
from collections import namedtuple
from django.test import TestCase

from ..factories import SpecFactory, JobFactory
from ..models import Job, Package, Spec
from ..tasks import query_pypi


def fake_distributions(*distributions):
    Distribution = namedtuple('Distribution', ['name', 'version'])
    result = []
    for dist in distributions:
        name, version = dist.split('==')
        result.append(Distribution(name, version))
    return result


def fake_requirement(name, specs):
    Requirement = namedtuple('Requirement', ['name', 'specs', 'extras'])
    return Requirement(name, specs, extras=[])


class JobTest(TestCase):

    def setUp(self):
        self.reqs_txt = """
            -r some_missing_file
            django>=1.4,<1.5
            Django-Geoip==0.3
            # tests below
            coverage
            coveralls>0.2
            # TODO: VCS
        """

    @patch('core.models.process_requirement.delay')
    def test_can_be_created_from_requirements_txt(self, req_task):
        with warnings.catch_warnings():
            # We're ignoring -r not being parsed
            # "Recursive requirements not supported. Skipping."
            warnings.simplefilter("ignore", category=UserWarning)
            job = Job.objects.create_from_requirements(self.reqs_txt)

        self.assertEqual(job.requirements, self.reqs_txt)
        self.assertEqual(req_task.call_count, 4)


class JobSepcTest(TestCase):

    def test_process_requirement(self):
        job = JobFactory()
        package, package_created, spec, spec_created = job.add_distribution(*fake_distributions('Django==1.5.4'))

        self.assertQuerysetEqual(Package.objects.all(), ['Django (django)'], transform=str, ordered=False)
        self.assertQuerysetEqual(job.specs.all(), ['Django==1.5.4'], transform=str, ordered=False)
        self.assertTrue(package_created)
        self.assertTrue(spec_created)

    def test_does_not_create_duplicate_specs(self):
        spec = SpecFactory(version='0.2.19', package__name='lettuce', package__slug='lettuce')
        job = JobFactory()
        same_package, package_created, same_spec, spec_created = job.add_distribution(*fake_distributions('lettuce==0.2.19'))

        self.assertFalse(package_created)
        self.assertFalse(spec_created)
        assert Spec.objects.count() == 1
        assert Package.objects.count() == 1
        assert job.specs.all().first().version == spec.version
        assert job.specs.all().first().package.name == spec.package.name
        assert spec.pk == same_spec.pk
        assert same_package.pk == same_spec.package.pk


class PypiTaskTest(TestCase):

    @patch('api.PyPI.get_info')
    def test_updates_spec(self, get_info_mock):
        last_release_date = timezone.now()
        py3_versions = ['3', '3.2', '3.3']
        get_info_mock.return_value = {
            'last_release_date': last_release_date,
            'py3_versions': py3_versions,
        }

        spec = SpecFactory(version='0.2.19', package__name='lettuce', package__slug='lettuce')
        self.assertEqual(query_pypi(spec.pk), get_info_mock.return_value)
        spec = Spec.objects.get(pk=spec.pk)
        assert spec.release_date == last_release_date
        assert spec.python_versions == py3_versions
