# coding: utf-8
from invoke import task, run


@task
def test():
    run('python manage.py test --with-doctest -a"!functional"'
        ' --with-specplugin --nocapture --nologcapture', pty=True)


@task
def functional(package=''):
    run('python manage.py test --with-specplugin -afunctional --nocapture --nologcapture %s' % package, pty=True)


@task
def cover(package='', only_unit=False):
    """ Django-nose does not report properly"""
    arg = '-a"!functional"' if only_unit else ''
    run('coverage run --source=%s manage.py test --with-doctest %s' % (package, arg), pty=True)
    run('coverage report -m', pty=True)


@task
def clean_pyc():
    run('find . -name \*.pyc -delete')
