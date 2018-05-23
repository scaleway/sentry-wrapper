sentry-wrapper Changelog
========================

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
