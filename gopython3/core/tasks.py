from celery.task import task
from core.models import Job, Spec
from api.wrappers import pypi


@task
def process_job(job_pk):
    """ Process single batch of packages

        For each package spec we execute following tasks:
            * PyPI query
            * GitHub query
            * Travis query
    """
    job = Job.objects.get(pk=job_pk)

    for jobspec in job.job_specs.all():
        query_pypi.delay(jobspec.spec.pk)


@task
def query_pypi(spec_pk):
    """ Query one spec of package on PyPI

        Sample result of PyPIWrapper:

        >>> pypi.PyPIWrapper().get_short_info('django', None)
        {'last_release_date': datetime.datetime(2013, 9, 15, 6, 30, 37),
         'name': 'Django',
         'python3_supported_versions': ['3', '3.2', '3.3'],
         'url': 'http://pypi.python.org/pypi/Django',
         'version': '1.5.4'}
    """
    spec = Spec.objects.get(pk=spec_pk)

    # query PyPI
    pkg_data = pypi.PyPIWrapper().get_short_info(spec.name, spec.version)

    spec.release_date = pkg_data['last_release_date']
    spec.python_versions = pkg_data['python3_supported_versions']
    spec.save()

    # Canonical package name case for the win
    if pkg_data['name'] != spec.name:
        package = spec.package
        package.name = pkg_data['name']
        package.save()

    return pkg_data
