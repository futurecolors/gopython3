import logging
from celery import group
from celery.task import task
from requirements.requirement import Requirement
from api import Github, PyPI, TravisCI
from core.models import Package, Spec, Line


logger = logging.getLogger(__name__)


@task
def process_requirement(line_id):
    """ Process requirement

        For each package spec we query following services:
            * PyPI
            * GitHub
            * Travis
    """
    line = Line.objects.get(pk=line_id)
    # we parse line again to reduce number of task args and stored metadata
    req = Requirement.parse(line.text)

    logger.info('Starting to process %s...' % req.name)

    # Freezing the requirement
    distribution = PyPI.get_distribution(req)
    # if no distribution is found, fail gracefully
    if not distribution:
        logger.warn('No distribution found for %s' % line.text)
        line.mark_as_failed()
        return

    package, package_created, spec, spec_created = line.set_distribution(distribution)

    # if spec is already parsed before, no need to do anything
    if not spec_created:
        logger.debug('Spec is already parsed before')
        return

    pypi = query_pypi.s(spec.pk)
    if req.specs:
        # If version is not fixed, we already got latest package
        # Otherwise, fetch latest package to see if it is py3 compatible
        # FIXME: Using a chord is not effective, but works, consider futures
        pypi = group(pypi, process_latest_spec.s(req.name, package.pk)) | aggregate_pypi_info.s()

    notify = notify_completed_spec.si(spec.pk)

    # if package was parsed before, no need to query github or travis again
    if not package_created:
        return (pypi | notify).delay()

    return (pypi | github_travis.s(package.pk) | notify).delay()


@task
def aggregate_pypi_info(*results):
    current = results[0][0]
    latest = results[0][1]
    if latest:  # can be None
        current.update(latest)
    return current


@task
def process_latest_spec(package_name, package_id):
    """ Process package latest version available on PyPI

        Obtaining only metadata from PyPI, because other tasks will query latest repo version anyway.
    """
    logger.debug('Creating latest spec')

    distribution = PyPI.get_distribution(package_name)
    latest_spec, created = Spec.objects.get_or_create(package_id=package_id, version=distribution.version)
    if created:
        # do not return spec, because it's already queued
        return query_pypi(latest_spec.pk)

@task
def query_pypi(spec_pk):
    """ Query one spec of package on PyPI"""
    spec = Spec.objects.get(pk=spec_pk)
    logger.debug('[PYPI] Fetching data for %s' % spec)
    pkg_data = PyPI().get_info(spec.name, spec.version)

    spec.release_date = pkg_data['last_release_date']
    spec.python_versions = pkg_data['py3_versions']
    spec.save(update_fields=['release_date', 'python_versions'])
    logger.debug('[PYPI] Finished %s ' % spec)

    return pkg_data


@task
def github_travis(pypi_results, package_id, shortcut=True):
    """ Get all relevant info form Github

        Github and Travis tasks can be processed in parallel
        Forks search is disabled, because ineffective yet
        But they need pypi info (to avoid GH search if possible)

        Pypi results example:
        {...
            'py3_versions': ['3', '3.2', '3.3'],
            'url': 'http://www.djangoproject.com/'
         ...}
    """
    # We don't need to query Github if package states py3 support on PyPI
    if pypi_results.get('py3_versions') and shortcut:
        logger.debug('[GITHUB] Skipping %s, PyPI says py3 is supported' % pypi_results['name'])
        return

    logger.debug('[GITHUB] Starting %s' % pypi_results['name'])
    gh_queries = group(get_repo_info.s(package_id),
                       get_issues.s(package_id) | get_pulls.s(package_id),
                       get_build_status.s(package_id))

    meta_url = pypi_results.get('url', '')
    full_name = Github().parse_url(meta_url)

    if full_name:
        logger.debug('Author has linked his package to %s, so we can skip search' % full_name)
        return gh_queries.delay(full_name)
    else:
        logger.debug('Initiating long way, url "%s" is not github' % meta_url)
        return (search_github.s(pypi_results['name']) | gh_queries).delay()


@task(rate_limit='20/m')
def search_github(package_name):
    """ Where are my sources, bro?

        Sometimes, package name is not the same as github repo name,
        but that should not be a problem, since Github search API
        is smart enough.

        Task is intentionally rate limited to avoid RateLimitExceeded with search beta API.
    """
    logger.debug('[GITHUB] Searching for repo of package %s ...' % package_name)
    full_name = Github().get_most_popular_repo(package_name)
    logger.debug('[GITHUB] Found package %s, full_name=%s' % (package_name, full_name))
    return full_name


@task
def get_repo_info(full_name, package_id):
    logger.debug('[GITHUB] Querying repo %s ...' % full_name)
    repo_info = Github().get_repo(full_name)

    Package.objects.filter(pk=package_id).update(
        repo_last_commit_date=repo_info['updated_at'],
        repo_url=repo_info['html_url']
    )
    logger.debug('[GITHUB] Finished repo query')
    return repo_info


@task
def get_forks(full_name, package_id):
    logger.debug('[GITHUB] Searching for forks of %s ...' % full_name)
    fork_info = Github().get_py3_forks(full_name)

    # Get url or first fork available or empty string
    fork_url = fork_info.pop(0, {}).get('html_url', '') if fork_info else ''
    Package.objects.filter(pk=package_id).update(
        fork_url=fork_url
    )
    logger.debug('[GITHUB] Finished fork query')
    return fork_info


@task
def get_issues(full_name, package_id):
    logger.debug('[GITHUB] Querying issues of %s ...' % full_name)
    issues_info = Github().get_py3_issues(full_name)

    issue_url = issues_info[0].get('html_url', '') if issues_info else ''
    issue_status = issues_info[0].get('state', '') if issues_info else ''
    Package.objects.filter(pk=package_id).update(
        issue_url=issue_url,
        issue_status=issue_status
    )
    logger.debug('[GITHUB] Finished issues query')
    return issues_info, full_name


@task
def get_pulls(issues_result, package_id):
    # Do not ask for pull-requests, if we got issues
    issues, full_name = issues_result
    if issues:
        return issues
    logger.debug('[GITHUB] Querying pull requests of %s ...' % full_name)
    pulls_info = Github().get_py3_pulls(full_name)
    pr_url = pulls_info[0].get('url', '') if pulls_info else ''
    pr_status = pulls_info[0].get('state') if pulls_info else 'unknown'
    Package.objects.filter(pk=package_id).update(
        pr_url=pr_url,
        pr_status=pr_status
    )
    logger.debug('[GITHUB] Finished pull request query')
    return pulls_info


@task
def get_build_status(full_name, package_id):
    logger.debug('[TRAVIS] Querying test build status of %s ...' % full_name)
    build_info = TravisCI().get_build_status(full_name)
    ci_url = build_info.get('html_url', '') if build_info else ''
    ci_status = build_info.get('last_build_state', 'unknown') if build_info else 'unknown'
    Package.objects.filter(pk=package_id).update(
        ci_url=ci_url,
        ci_status=ci_status
    )
    logger.debug('[TRAVIS] Finished query')

    return build_info


@task
def notify_completed_spec(spec_id):
    """ Spec processing has finished, now we need to record the result """
    spec = Spec.objects.get(pk=spec_id)
    spec.do_finish()
    logger.info('✓ %s finished' % spec)
