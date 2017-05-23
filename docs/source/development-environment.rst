Zipline Development Guidelines
==============================

Environment Setup
-----------------

First, you'll need to clone zipline by running:

.. code-block:: bash

   git clone git@github.com:quantopian/zipline.git

Then check out to a new branch where you can make your changes:

.. code-block:: bash
		
   git checkout -b some-short-descriptive-name

The following section assumes you already have virtualenvwrapper and pip installed on your system. If you don't already have them, you'll need some C library dependencies. On Linux you can run:

.. code-block:: bash

   # on linux
   $ sudo apt-get install libopenblas-dev liblapack-dev gfortran

   
   $ wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
   $ tar -xvzf ta-lib-0.4.0-src.tar.gz
   $ cd ta-lib/
   $ ./configure --prefix=/usr
   $ make
   $ sudo make install

And for `ta-lib` on OS X you can just run: `brew install ta-lib`.

Suggested installation of Python library dependencies used for development:

.. code-block:: bash

   $ mkvirtualenv zipline
   $ ./etc/ordered_pip.sh ./etc/requirements.txt
   $ pip install -r ./etc/requirements_dev.txt
   $ pip install -r ./etc/requirements_blaze.txt 
   $ pip install -r ./etc/requirements_talib.txt 
   $ pip install coverage coveralls

Finally, you can install zipline in development mode by running:

.. code-block:: bash

   python setup.py built_ext --inplace


Style Guide & Running Tests
---------------------------

We use `flake8` for checking style requirements and `nosetests` to run zipline tests.

Before submitting patches or pull requests, please ensure that your changes pass when running:

.. code-block:: bash

   $ flake8 zipline

and

.. code-block:: bash
		
   $ nosetests --with-coverage


If you get an error running nosetests after setting up a fresh virtualenv, please try running deactivate zipline; workon zipline, where zipline is the name of your virtualenv.

   
Docs
----

To build and view the docs locally, run:

.. code-block:: bash

   $ cd docs
   $ make html
   $ {BROWSER} build/html/index.html


Commit messages
---------------

Standard acronyms to start the commit message with are:

.. code-block:: bash
 
   BLD: change related to building zipline
   BUG: bug fix
   DEP: deprecate something, or remove a deprecated object
   DEV: development tool or utility
   DOC: documentation
   ENH: enhancement
   MAINT: maintenance commit (refactoring, typos, etc.)
   REV: revert an earlier commit
   STY: style fix (whitespace, PEP8)
   TST: addition or modification of tests
   REL: related to releasing Zipline
   PERF: Performance enhancements


Some commit style guidelines:

Commit lines should be no longer than [72 characters](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project). The first line of the commit should include one of the above prefixes. There should be an empty line between the commit subject and the body of the commit. In general, the message should be in the imperative tense. Best practice is to include not only what the change is, but why the change was made.

e.g.

.. code-block:: bash

   MAINT: Remove unused calculations of max_leverage, et al.

   In the performance period the max_leverage, max_capital_used,
   cumulative_capital_used were calculated but not used.

   At least one of those calculations, max_leverage, was causing a
   divide by zero error.
   
   Instead of papering over that error, the entire calculation was
   a bit suspect so removing, with possibility of adding it back in
   later with handling the case (or raising appropriate errors) when
   the algorithm has little cash on hand.

Pulling in Pull Requests (PRs)
------------------------------

.. code-block:: bash

   (master) $ git checkout -b PR-135
   $ curl https://github.com/quantopian/zipline/pull/135.patch | git am
   # Clean up commit history
   $ git rebase -i master
   # Merge (use no-ff for many commits and ff for few)
   $ git merge --no-ff --edit


