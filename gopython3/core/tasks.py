from celery.task import task
from api2.pypi import PyPI


@task
def process_requirement(req, job_id):
    """ Process requirement

        Receives a named tuple of parsed requirement:
        >>> req.name, req.specs, req.extras
        ('Django', [('>=', '1.5'), ('<', '1.6')], [])
    """
    from .models import JobSpec

    distribution = PyPI.get_distribution(req)
    job_spec = JobSpec.objects.create_from_distribution(distribution, job_id)

    query_pypi.delay(job_spec.spec.pk)
    if not req.specs:
        # If version is not fixed, we already got latest package
        (create_latest_spec.s(req.name, job_spec.spec.package.pk) | query_pypi.s())


@task
def create_latest_spec(package_name, package_id):
    """ Locate latest version available on PyPI """
    from .models import Spec

    distribution = PyPI.get_distribution(package_name)
    latest_spec, _ = Spec.objects.get_or_create(package_id=package_id, version=distribution.version)
    return latest_spec.pk


@task
def query_pypi(spec_pk):
    """ Query one spec of package on PyPI"""
    from .models import Spec

    spec = Spec.objects.get(pk=spec_pk)
    pkg_data = PyPI().get_info(spec.name, spec.version)

    spec.release_date = pkg_data['last_release_date']
    spec.python_versions = pkg_data['py3_versions']
    spec.save(update_fields=['release_date', 'python_versions'])

    return pkg_data

