# coding: utf-8
from invoke import task, run


@task
def test():
    run('python manage.py test --with-specplugin', pty=True)


@task
def cover(package=''):
    """ Django-nose does not report properly"""
    run('coverage run --source=%s manage.py test' % package, pty=True)
    run('coverage report -m', pty=True)
