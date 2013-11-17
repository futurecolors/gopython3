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

    def test_can_be_created_from_requirements_txt(self):
        with warnings.catch_warnings():
            # We're ignoring -r not being parsed
            # "Recursive requirements not supported. Skipping."
            warnings.simplefilter("ignore", category=UserWarning)
            job = Job.objects.create_from_requirements(self.reqs_txt)

        assert job.requirements == self.reqs_txt
        assert list(map(str, job.lines.all().order_by('pk'))) == [
            'django>=1.4,<1.5',
            'Django-Geoip==0.3',
            'coverage',
            'coveralls>0.2']


class JobStatusTest(TestCase):

    def test_completed_if_no_specs_no_lines(self):
        job = JobFactory()
        assert job.status == 'success', 'No specs, no lines'

    def test_pending_if_unparsed_lines(self):
        job = JobFactory(lines=['spanish=42,inquisition==7'])
        assert job.status == 'pending', 'It has 2 unparsed lines'

    def test_pending_if_pending_specs(self):
        job = JobFactory(specs=['foo=1,bar==2'])
        assert job.status == 'running', 'It has 2 unfinished specs, but lines are parsed'

    def test_running_if_running_and_finished_specs(self):
        job = JobFactory(specs=['foo=1,bar==2'])
        spec = job.specs.first()
        spec.status = 'running'
        spec.save()
        job = Job.objects.get(pk=job.pk)
        assert job.status == 'running', 'Job has started, but has not finished yet'

    def test_running_if_one_spec_pending(self):
        job = JobFactory(specs=['foo=1,bar==2'])
        job.specs.all().update(status='success')
        job = Job.objects.get(pk=job.pk)
        assert job.status == 'success', 'One spec pending'

    def test_running_if_finished_and_pending_specs(self):
        job = JobFactory(specs=['steve==1', 'jobs==2'])
        spec = job.specs.first()
        spec.status = 'finished'
        spec.save()
        assert job.status == 'running', 'One spec has finished, but 1 line is not parsed yet'

    def test_completed_if_specs_completed(self):
        job = JobFactory(specs=['foo=1,bar==2'])
        job.specs.all().update(status='success')
        job = Job.objects.get(pk=job.pk)
        assert job.status == 'success', 'All specs have finished'


class JobSpecTest(TestCase):

    def test_process_requirement(self):
        job = JobFactory(lines=['Django==1.5.4'])
        package, package_created, spec, spec_created = job.lines.all()[0].set_distribution(*fake_distributions('Django==1.5.4'))

        assert list(map(str, Package.objects.all())) == ['Django']
        assert list(map(str, job.specs.all())) == ['Django==1.5.4']
        assert package_created
        assert spec_created

    def test_does_not_create_duplicate_specs(self):
        spec = SpecFactory(version='0.2.19', package__name='lettuce')
        job = JobFactory(lines=['lettuce==0.2.19'])
        same_package, package_created, same_spec, spec_created = job.lines.all()[0].set_distribution(*fake_distributions('lettuce==0.2.19'))

        assert not package_created
        assert not spec_created
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

        spec = SpecFactory(version='0.2.19', package__name='lettuce')
        assert query_pypi(spec.pk) == get_info_mock.return_value
        spec = Spec.objects.get(pk=spec.pk)
        assert spec.release_date == last_release_date
        assert spec.python_versions == py3_versions
