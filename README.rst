DESCRIPTION
===========

sentry-wrapper calls a setuptools entrypoint and sends exceptions to sentry. It
is useful to log the exceptions of a correctly-packaged-but-not-sentry-capable
program.


Usage::

    usage: sentry-wrapper [-h] [--dsn SENTRY_DSN] name [dist] [group] [-- ...]

    positional arguments:
      name              Entry point name (eg. my-entrypoint)
      dist              Distribution name (eg. my-project==1.2.4, default: same
                        value than name)
      group             Entry point group (default: console-scripts)

    optional arguments:
      -h, --help        show this help message and exit
      --dsn SENTRY_DSN  Sentry DSN

    Extra arguments are given as is to the wrapped entrypoint.


INSTALLATION
============

To install in a virtualenv::

    $> virtualenv myenv
    $> source myenv/bin/activate
    $> pip install sentry-wrapper


DEVELOP
=======

To start hacking on sentry-wrapper::

    $> virtualenv myenv
    $> source myenv/bin/activate
    $> git clone git@github.com:brmzkw/sentry-wrapper.git
    $> cd sentry-wrapper
    $> pip install -e .


CONTRIBUTORS
============

* `Bastien Chatelard <https://github.com/bchatelard/>`_
* `Julien Castets <https://github.com/brmzkw/>`_
