Go Python 3
===========

.. image:: https://coveralls.io/repos/futurecolors/djangodash2013/badge.png?branch=dev
  :target: https://coveralls.io/r/futurecolors/djangodash2013?branch=dev

Dear geeks, the time has come to migrate all your projects to Python 3.
We'll help you update your dependencies, and you need to migrate only your own code.

http://gopython3.com/
---------------------

For those of you REST lovers:

API: http://gopython3.com/api/v1
Docs: http://docs.python3.apiary.io/

Install
-------

Steps to get it running locally (virtualenv is implied and ommited):

    git clone git@github.com:futurecolors/djangodash2013.git
    cd djangodash2013/gopython3
    pip install -r requirements.txt
    manage.py syncdb
    npm install # less templates
    manage.py runserver
    manage.py celeryd

For production environments following variables are required:

    export DJANGO_CONFIGURATION = Prod
    export DJANGO_BROKER_URL = foo
    export DATABASE_URL = bar
    export DJANGO_SECRET_KEY = baz
    export DJANGO_GITHUB_CLIENT_ID = xxx
    export DJANGO_GITHUB_CLIENT_SECRET = yyy
