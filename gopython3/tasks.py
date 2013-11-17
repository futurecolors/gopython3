# coding: utf-8
from invoke import task, run

#traceback print mode (long/short/line/native/no)
test_command = 'PYTHONPATH=`pwd` NO_PROXY=1 py.test'

@task
def test():
    run(test_command + ' -m \'not functional\'', pty=True)


@task
def functional(package=''):
    run(test_command + ' -m \'functional\' %s' % package, pty=True)


@task
def cover(package='.', only_unit=False):
    testing_type = ' -m \'not functional\'' if only_unit else ''
    run(test_command + ' --cov %s' % package + testing_type)


@task
def clean_pyc():
    run('find . -name \*.pyc -delete')
