# coding: utf-8
from invoke import task, run


@task
def test():
    run('python manage.py test --with-specplugin --failed', pty=True)
