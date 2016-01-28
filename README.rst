.. image:: https://travis-ci.org/strizhechenko/twitterbot_utils.svg?branch=master


Twitterbot utils

Useful functions for everyone who want to write one more xxx everyword bot.

By the `Oleg Strizhechenko <oleg.strizhechenko@gmail.com>`_

============
Introduction
============

This library provides bunch of functions for tasks on creating twitter bots.

==========
Installing
==========

You can install twitterbot-utils using::

    $ pip install twitterbot-utils

================
Getting the code
================

The code is hosted at https://github.com/strizhechenko/twitterbot_utils

Check out the latest development version anonymously with::

    $ git clone git://github.com/strizhechenko/twitterbot_utils.git
    $ cd twitterbot_utils

Setup a virtual environment and install dependencies:

	$ make env

Activate the virtual environment created:

	$ source env/bin/activate

=============
Running Tests
=============
No test on current state avaible.

=============
Documentation
=============

Authorize your bot:

        source env/bin/activate
        export consumer_key=xxx
        export consumer_secret=xxy
        python -m twitterbot_utils.TwiAuth

When, copy PIN and get your access token/secret to put in heroku config.

=====
TODO
=====

Usage, docs, tests.
