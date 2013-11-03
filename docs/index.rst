Go Python 3
===========

We want to help developers migrate their projects to python3.
Because most of the code is usually contained in dependencies,
we strive to provide maximum info about libraries status of python 3 support.

.. toctree::
   :maxdepth: 2

How it works
------------
User submits his ``requirements.txt`` to learn, how many packages have python 3 support.
We create a ``Job``, separated into package ``Specs``, one for each row of the file.
For each spec we are pulling these actions:

    * resolve package dependency if spec is not frozen
    * check cache, if we have already processed the Spec in the past
    * ask PyPI for package metadata, if python 3 support is found in classifiers, we're done
    * guess where the repo is, first, from PyPI metadata.
    * if we don't know where the repo is, search github for this package.
    * query for open issues or pull requests
    * query for forks (currently, ``ineffective``)
    * query Travis for tests (or, maybe, python versions under test)

Tests
-----
::

    pip install invoke
    invoke test # unittests
    invoke functional # functional tests

Note, that functional tests might fail if you hit rate limit.



