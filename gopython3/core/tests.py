import warnings
from django.test import TestCase
from .models import Job, Package, Spec, JobSpec


class JobTest(TestCase):

    def test_can_be_created_from_requirements_txt(self):
        reqs_txt = """
            -r some_missing_file
            django>=1.4,<1.5
            Django-Geoip==0.3
            # tests below
            coverage
            coveralls>0.2
            # TODO: VCS
            nose==1.3
        """
        with warnings.catch_warnings():
            # We're ignoring -r not being parsed
            # "Recursive requirements not supported. Skipping."
            warnings.simplefilter("ignore", category=UserWarning)
            job = Job.objects.create_from_requirements(reqs_txt)

        assert job.requirements == reqs_txt
        self.assertQuerysetEqual(Package.objects.all(),
                                 ['Django-Geoip (django_geoip)', 'nose (nose)'], transform=str, ordered=False)
        self.assertQuerysetEqual(Spec.objects.all(),
                                 ['Django-Geoip==0.3', 'nose==1.3'], transform=str, ordered=False)
        self.assertQuerysetEqual(JobSpec.objects.all(),
                                 ['Job 1 [pending] nose==1.3', 'Job 1 [pending] Django-Geoip==0.3'],
                                 transform=str, ordered=False)
