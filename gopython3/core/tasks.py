from celery import group
from celery.task import task
from api2 import Github, PyPI, TravisCI


@task
def process_requirement(req, job_id):
    """ Process requirement

        For each package spec we query following services:
            * PyPI
            * GitHub
            * Travis
    """
    from .models import JobSpec

    # Freezing the requirement
    distribution = PyPI.get_distribution(req)
    job_spec = JobSpec.objects.create_from_distribution(distribution, job_id)

    # TODO: if spec is already parsed, halt

    pypi = query_pypi.s(job_spec.spec.pk)
    if req.specs:
        # If version is not fixed, we already got latest package
        process_latest_spec.s(req.name, job_spec.spec.package.pk) | query_pypi.s()

    # Github and Travis tasks can be processed in parallel
    # But they need pypi info (to avoid GH search if possible)
    github_travis = group(get_repo_info.s(),
                          get_issues.s() | get_pulls.s(),
                          get_build_status.s())

    notify = notify_completed_spec.si(job_spec)

    return (pypi | github_travis | notify).delay()


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


@task
def get_repo_info(full_name):
    """ What's with my sources, bro? """
    return Github().get_repo(full_name)


@task
def get_forks(full_name):
    return Github().get_py3_forks(full_name)


@task
def get_issues(full_name):
    return Github().get_py3_issues(full_name)


@task
def get_pulls(issues, full_name):
    # Do not ask for pull-requests, if we got issues
    if issues:
        return issues
    return Github().get_py3_pulls(full_name)


@task
def get_build_status(full_name):
    """ How are my tests going? """
    return TravisCI().get_build_status(full_name)


@task
def notify_completed_spec(spec_id):
    """ Spec processing has finished, now we need to record the result
    """
    from .models import Spec
    spec = Spec.objects.get(pk=spec_id)
    spec.do_finish()
