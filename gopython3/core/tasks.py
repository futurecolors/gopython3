from celery import chain, group, chord
from celery.task import task
from api.wrappers.github import parse_github_url
from core.models import Job, Spec, Package, JobSpec
from api.wrappers import pypi, github, travis


@task
def process_job(job_pk):
    """ Process single batch of packages

        For each package spec we execute following tasks:
            * PyPI query
            * GitHub query
            * Travis query
    """
    job = Job.objects.get(pk=job_pk)
    job.do_start()

    return chord(process_spec.s(job_spec.pk)
                 for job_spec in JobSpec.objects.filter(job=job))(notify_completed_job.si(job_pk))


@task
def process_spec(job_spec_pk):
    """ Process jobspec"""
    job_spec = JobSpec.objects.get(pk=job_spec_pk)
    job_spec.do_start()

    package, version = job_spec.spec.package, job_spec.spec.version
    finished_specs = Spec.objects.filter(package=package, version=version, status='finished').exists()
    if finished_specs:  # not asking services if already parsed
        return notify_completed_spec.delay(job_spec_pk)
    else:
        return chain(query_pypi.s(job_spec.spec.pk),
                     query_github.s(job_spec.spec.package.pk),
                     notify_completed_spec.si(job_spec_pk)).delay()


@task
def notify_completed_job(job_pk):
    """ Job has finished, now we need to record the result"""
    job = Job.objects.get(pk=job_pk)
    job.do_finish()


@task
def notify_completed_spec(job_spec_pk):
    """ Job has finished, now we need to record the result
    """
    job_spec = JobSpec.objects.get(pk=job_spec_pk)
    spec = job_spec.spec
    spec.status = 'completed'
    spec.save(update_fields=['status'])
    job_spec.do_finish()


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
    pypi_api = pypi.PyPIWrapper()
    pkg_data = pypi_api.get_short_info(spec.name, spec.version)
    latest_pkg_data = pypi_api.get_short_info(spec.name)

    spec.release_date = pkg_data['last_release_date']
    spec.python_versions = pkg_data['python3_supported_versions']

    spec.latest_version = latest_pkg_data['version']
    spec.latest_release_date = latest_pkg_data['last_release_date']
    spec.latest_python_versions = latest_pkg_data['python3_supported_versions']
    spec.save()

    # Canonical package name case for the win
    if pkg_data['name'] != spec.name:
        package = spec.package
        package.name = pkg_data['name']
        package.save()

    return pkg_data


@task
def search_github(package_name, url):
    """ Where are my sources, bro?

        Sometimes, package name is not the same as github repo name,
        but that should not be a problem, since Github search API
        is smart enough.

        >>> github.GithubSearchWrapper().get_most_popular_repo('moscowdjango')
        ('moscowdjango', 'futurecolors')
    """
    if url:
        repo_info = parse_github_url(url)
        if repo_info:
            # query directly to github account
            return repo_info['repo_name'], repo_info['owner']

    repo_name, owner = github.GithubSearchWrapper().get_most_popular_repo(package_name)
    return repo_name, owner


@task
def get_short_info(repo_tuple):
    """ What's with my sources, bro?

        >>> github.GithubWrapper().get_short_info('futurecolors', 'moscowdjango')
        {'updated_at': datetime.datetime(2013, 9, 15, 6, 30, 37),
         'url': 'https://api.github.com/repos/futurecolors/moscowdjango'}
    """
    repo_name, owner = repo_tuple  # FIXME
    return github.GithubWrapper().get_short_info(owner, repo_name)


@task
def get_forks(repo_tuple):
    repo_name, owner = repo_tuple
    return github.GithubWrapper().get_py3_fork_info(owner, repo_name)


@task
def get_issues(repo_tuple):
    repo_name, owner = repo_tuple
    return github.GithubWrapper().get_py3_issues_info(owner, repo_name)


@task
def get_pr(repo_tuple):
    repo_name, owner = repo_tuple
    return github.GithubWrapper().get_py3_pull_requests(owner, repo_name)


@task
def get_build_status(repo_tuple):
    """ How are my tests going? """
    repo_name, owner = repo_tuple
    travis_data = travis.TravisCI().get_build_status(owner, repo_name)

    return travis_data


@task
def notify_github_completed(r, package_pk):
    """ Update github package info in database"""
    package = Package.objects.get(pk=package_pk)
    package.repo_last_commit_date = r[0].get('updated_at')
    package.repo_url = r[0].get('url')

    # For now we'll take the first one available
    package.pr_url = r[1][0].get('url', '') if r[1] else ''
    package.pr_status = r[1][0].get('state') if r[1] else 'unknown'

    package.issue_url = r[2][0].get('url', '') if r[2] else ''
    package.issue_status = r[2][0].get('state') if r[2] else 'unknown'

    package.fork_url = r[3][0].pop(0, {}).get('url', '') if r[3] else ''

    # Travis
    package.ci_url = r[3].get('url', '') if r[4] else ''
    package.ci_status = r[3].get('last_build_status', 'unknown') if r[4] else 'unknown'
    package.save()
    return r


@task
def query_github(results, package_pk):
    """ Get all relevant info form Github"""
    package = Package.objects.get(pk=package_pk)

    # GH API queries running in parallel for speedup
    gh_queries = group(get_short_info.s(),
                       get_pr.s(),
                       get_issues.s(),
                       get_forks.s(),
                       get_build_status.s())

    # guessing github url and querying info
    return chain(search_github.s(package.name, results.get('url')),
                 gh_queries,
                 notify_github_completed.s(package_pk)).delay()
