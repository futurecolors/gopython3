Go Python 3
===========

Dear geeks, the time has come to migrate all your projects to Python 3.
We'll help you update your dependencies, and you need to migrate only your own code.

Install
--------

Steps to get it running locally:

    git clone
    pip install
    manage.py syncdb
    npm install
    manage.py runserver
    manage.py celeryd

For production environments:

    export DJANGO_CONFIGURATION = Prod
    export DJANGO_BROKER_URL = foo
    export DATABASE_URL = bar
    export DJANGO_SECRET_KEY = baz
    export DJANGO_GITHUB_CLIENT_ID = xxx
    export DJANGO_GITHUB_CLIENT_SECRET = yyy
