Go Python 3
===========

We want to help developers migrate their projects to python3.
Because most of the code is usually contained in dependencies,
we strive to provide maximum info about libraries status of python 3 support.

.. toctree::
   :maxdepth: 2

API
----

For those of you REST lovers:

API: http://gopython3.com/api/v1/

API Docs: http://docs.python3.apiary.io/

Install
-------

Steps to get it running locally (virtualenv is implied and ommited)::

    git clone git@github.com:futurecolors/djangodash2013.git
    cd djangodash2013/gopython3
    pip install -r requirements.txt
    manage.py syncdb
    npm install # less templates
    manage.py runserver
    manage.py celeryd

Production
~~~~~~~~~~

For production environments following variables are required::

    export DJANGO_CONFIGURATION = Prod
    export DJANGO_BROKER_URL = foo
    export DATABASE_URL = bar
    export DJANGO_SECRET_KEY = baz
    export DJANGO_GITHUB_CLIENT_ID = xxx
    export DJANGO_GITHUB_CLIENT_SECRET = yyy
