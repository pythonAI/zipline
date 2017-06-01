Zipline Development Guidelines
==============================
This page is intended for developers of Zipline, people who want to contribute to the Zipline codebase or documentation, or people who want to install from source and make local changes to their copy of Zipline.

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome. We [track issues](https://github.com/quantopian/zipline/issues) on [GitHub](https://github.com/) and also have a [mailing list](https://groups.google.com/forum/#!forum/zipline) where you can ask questions.


Creating a Development Environment
----------------------------------

First, you'll need to clone Zipline by running:

.. code-block:: bash

   git clone git@github.com:your-github-username/Zipline.git

Then check out to a new branch where you can make your changes:

.. code-block:: bash
		
   git checkout -b some-short-descriptive-name

The following section assumes you already have virtualenvwrapper and pip installed on your system. If you don't already have them, you'll need some C library dependencies. You can follow the [install guide](http://www.Zipline.io/install.html) to get the appropriate dependencies.

In order to run tests locally, you'll need TA-lib.
.. code-block:: bash

   $ wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
   $ tar -xvzf ta-lib-0.4.0-src.tar.gz
   $ cd ta-lib/
   $ ./configure --prefix=/usr
   $ make
   $ sudo make install

And for `TA-lib` on OS X you can just run: `brew install ta-lib`.

Suggested installation of Python library dependencies used for development:

.. code-block:: bash

   $ mkvirtualenv Zipline
   $ ./etc/ordered_pip.sh ./etc/requirements.txt
   $ pip install -r ./etc/requirements_dev.txt
   $ pip install -r ./etc/requirements_blaze.txt 
   $ pip install -r ./etc/requirements_talib.txt 

Finally, you can build the C extensions by running:

.. code-block:: bash

   $ python setup.py build_ext --inplace

To finish, make sure tests pass by running

.. code-block:: bash

   $ nosetests

If you get an error running nosetests after setting up a fresh virtualenv, please try running

.. code-block:: bash

   # where Zipline is the name of your virtualenv
   $ deactivate Zipline

   $ workon Zipline


Development with Docker
-----------------------

If you want to work with zipline using a [Docker](https://docs.docker.com/get-started/) container, you'll need to build the `Dockerfile` in the Zipline root directory, and then build `Dockerfile-dev`. Instructions for building both containers can be found in `Dockerfile` and `Dockerfile-dev`, respectively.


Style Guide & Running Tests
---------------------------

We use `flake8` for checking style requirements and `nosetests` to run Zipline tests. Our [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration) tools will run these commands.

Before submitting patches or pull requests, please ensure that your changes pass when running:

.. code-block:: bash

   $ flake8 Zipline tests

In order to run tests locally, you'll need TA-lib, which you can install on Linux by running:

.. code-block:: bash

   $ wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
   $ tar -xvzf ta-lib-0.4.0-src.tar.gz
   $ cd ta-lib/
   $ ./configure --prefix=/usr
   $ make
   $ sudo make install

And for `TA-lib` on OS X you can just run: `brew install ta-lib`.

You should now be free to run tests:

.. code-block:: bash
		
   $ nosetests


Continuous Integration
----------------------

We use [Travis CI](https://travis-ci.org/) for Linux builds and [AppVeyor](https://www.appveyor.com/) for Windows builds; we do not currently have CI for OS X builds.


Packaging
---------
To learn about how we build Zipline packages on [Anaconda](https://anaconda.org/), you can read [this](http://www.Zipline.io/release-process.html#uploading-conda-packages) section in our release process notes.

   
Contributing to the Docs
------------------------

If you'd like to contribute to the documentation, you can navigate to `docs/source/` where each [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) or `.rst` file is a separate section here on zipline.io. To add a section, create a new file called `some-descriptive-name.rst` and add `some-descriptive-name` to `appendix.rst`. To edit a section, simply open up one of the existing files, make your changes, and save them.

We use [Sphinx](http://www.sphinx-doc.org/en/stable/) to generate documentation for Zipline.

To build and view the docs locally, run:

.. code-block:: bash

   # assuming you're in the Zipline root directory
   $ cd docs
   $ make html
   $ {BROWSER} build/html/index.html


Commit messages
---------------

Standard prefixes to start a commit message:

.. code-block:: bash

   BLD: change related to building Zipline
   BUG: bug fix
   DEP: deprecate something, or remove a deprecated object
   DEV: development tool or utility
   DOC: documentation
   ENH: enhancement
   MAINT: maintenance commit (refactoring, typos, etc)
   REV: revert an earlier commit
   STY: style fix (whitespace, PEP8, flake8, etc)
   TST: addition or modification of tests
   REL: related to releasing Zipline
   PERF: performance enhancements


Some commit style guidelines:

Commit lines should be no longer than [72 characters](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project). The first line of the commit should include one of the above prefixes. There should be an empty line between the commit subject and the body of the commit. In general, the message should be in the imperative tense. Best practice is to include not only what the change is, but why the change was made.

e.g.

.. code-block:: text

   MAINT: Remove unused calculations of max_leverage, et al.

   In the performance period the max_leverage, max_capital_used,
   cumulative_capital_used were calculated but not used.

   At least one of those calculations, max_leverage, was causing a
   divide by zero error.
   
   Instead of papering over that error, the entire calculation was
   a bit suspect so removing, with possibility of adding it back in
   later with handling the case (or raising appropriate errors) when
   the algorithm has little cash on hand.


Formatting Docstrings
---------------------

When adding or editing docstrings for classes, functions, etc, we use the numpy [HOWTO_DOCUMENT](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt) file as the canonical reference.


Pulling in Pull Requests (PRs)
------------------------------

.. code-block:: bash

   (master) $ git checkout -b PR-135
   $ curl https://github.com/quantopian/Zipline/pull/135.patch | git am

   # Clean up commit history
   $ git rebase -i master

   # Merge (use no-ff for many commits and ff for few)
   $ git merge --no-ff --edit


