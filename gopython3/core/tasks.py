from celery import chain, group
from celery.task import task
from core.models import Job, Spec, Package
from api.wrappers import pypi, github


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


@task
def search_github(package_name):
    """ Where are my sources, bro?

        Sometimes, package name is not the same as github repo name,
        but that should not be a problem, since Github search API
        is smart enough.

        >>> github.GithubSearchWrapper().get_most_popular_repo('moscowdjango')
        ('moscowdjango', 'futurecolors')
    """
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
def notify_github_completed(r, package_pk):
    """ Update github package info in database"""
    package = Package.objects.get(pk=package_pk)
    package.repo_last_commit_date = r[0].get('updated_at')
    package.repo_url = r[0].get('url')

    # For now we'll take the first one available
    package.pr_url = r[1].pop(0).get('issue_url', '') if r[1] else ''
    #package.pr_status = r[1].get('issue_url')

    package.issue_url = r[2].pop(0).get('issue_url', '') if r[2] else ''
    #package.issue_status = r[2].get('issue_url')

    package.fork_url = r[3].pop(0, {}).get('issue_url', '') if r[3] else ''
    #package.fork_status = r[3].get('issue_url')
    package.save()
    return r


@task
def query_github(package_pk):
    """ Get all relevant info form Github"""
    package = Package.objects.get(pk=package_pk)

    # if github url is available
    if False:
        # query directly to github account
        pass
    else:
        # GH API queries running in parallel for speedup
        gh_queries = group(get_short_info.s(),
                           get_pr.s(),
                           get_issues.s(),
                           get_forks.s()
                          )

        # guessing github url and querying info
        return chain(search_github.s(package.name),
                     gh_queries,
                     notify_github_completed.s(package_pk)).delay()
