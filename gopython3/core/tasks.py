from celery.task import task
from distlib.locators import locate
from api2.pypi import PyPI


@task
def process_requirement(req, job_id):
    """ Process requirement

        Receives a named tuple of parsed requirement:
        >>> req.name, req.specs, req.extras
        ('Django', [('>=', '1.5'), ('<', '1.6')], [])
    """
    from .models import Package, Spec, JobSpec

    # E.g.: Django (>= 1.0, < 2.0, != 1.3
    distlib_line = req.name
    if req.specs:
        distlib_line += ' (%s)' % (', '.join('%s %s' % cond for cond in req.specs))
        skip_locate_latest = False
    else:
        skip_locate_latest = True

    # Returned object has canonical name (flask -> Flask)
    distribution = locate(distlib_line)

    # Create models
    package, _ = Package.objects.get_or_create(name=distribution.name)
    spec, _ = Spec.objects.get_or_create(package=package, version=distribution.version)
    JobSpec.objects.create(job_id=job_id, spec=spec)

    query_pypi.delay(spec.pk)
    if not skip_locate_latest:
        (create_latest_spec.s(req.name, package.pk) | query_pypi.s())

@task
def create_latest_spec(package_name, package_id):
    """ Locate latest version available on PyPI """
    from .models import Spec

    distribution = locate(package_name)
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

