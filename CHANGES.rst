sentry-wrapper Changelog
========================

2.4.0 (2019-07-05)
------------------

* Replace raven (deprecated) by sentry-sdk

2.3.0 (2018-11-16)
------------------

I messed up release 2.2.0 and pushed a package on pypi with the wrong version.
2.3.0 is the correct version to use.


2.2.0 (never released)
----------------------

* Add a script which send message to sentry::

        sentry-msg --dsn https://... "my message to send"


2.1.1 (unreleased)
------------------

* Under very active development.

2.1.0 (2018-05-23)
------------------

* Add flag `-t` or `--timeout`. After the specified amount of time,
  sentry-wrapper exits and raises an error to Sentry.
  This is implemented by raising SIGALARM. If the wrapped application catches
  the signal, timeout won't work.

2.0.0 (2015-08-20)
------------------

* Accept extra arguments that are given to the wrapped command, like::

        sentry-wrapper entrypoint -- arg1 arg2 arg3

1.0.0 (2015-04-20)
------------------

* Initial version.
