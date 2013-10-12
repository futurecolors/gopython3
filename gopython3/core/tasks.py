from celery.task import task
from api2.github import Github
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
        (process_latest_spec.s(req.name, job_spec.spec.package.pk) | query_pypi.s())


@task
def process_latest_spec(package_name, package_id):
    """ Process package latest version available on PyPI

        Obtaining only metadata from PyPI, because other tasks will query latest repo version anyway.
    """
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


@task(rate_limit='20/m')
def search_github(package_name, url=False):
    """ Where are my sources, bro?

        Sometimes, package name is not the same as github repo name,
        but that should not be a problem, since Github search API
        is smart enough.

        Task is intentionally rate limited to avoid RateLimitExceeded with search beta API.
    """
    if url:
        full_name = Github().parse_url(url)
        if full_name:
            # query directly to github account, skipping search
            return full_name

    full_name = Github().get_most_popular_repo(package_name)
    return full_name

