DESCRIPTION
===========

sentry-wrapper calls a setuptools entrypoint and sends exceptions to sentry. It
is useful to log the exceptions of a correctly packaged but not sentry-capable
program.


Usage::

    usage: sentry-wrapper [options] [-- entrypoint options]

    positional arguments:
      name                  Entry point name (eg. my-entrypoint)
      dist                  Distribution name (eg. my-project==1.2.4, default:
                            same value than name)
      group                 Entry point group (default: console_scripts)

    optional arguments:
      -h, --help            show this help message and exit
      --dsn SENTRY_DSN      Sentry DSN
      -t timeout, --timeout timeout
                            Timeout. After this value, TimeoutError is raised to
                            Sentry.


For example, if the `setup.py` file of the package `mypackage` contains::

    ...
    name='my-package',
    entry_points={
        'console_scripts': [
            'my-entrypoint = mypackage:main',
        ],
    },
    ...

Call `my-entrypoint` with::

    sentry-wrapper --dsn SENTRY_DSN my-entrypoint my-package console_scripts


INSTALLATION
============

To install in a virtualenv::

    $> virtualenv myenv
    $> source myenv/bin/activate
    $> pip install sentry-wrapper
    $> pip install path/to/your/project
    $> sentry-wrapper -h


DEVELOP
=======

To start hacking on sentry-wrapper using Docker::

    $> make

Then:

- Visit http://localhost:9000 with the credentials test/test
- Create a project and copy the DSN
- Test sentry-wrapper against the test project of this repository::

    sentry-wrapper --dsn [...] whatever_ok whatever console_scripts
    sentry-wrapper --dsn [...] whatever_exception whatever console_scripts

CONTRIBUTORS
============

* `Bastien Chatelard <https://github.com/bchatelard/>`_
* `Julien Castets <https://github.com/brmzkw/>`_
