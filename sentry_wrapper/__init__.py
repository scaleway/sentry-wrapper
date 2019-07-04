import argparse
import os
import signal
import sys

import pkg_resources

import sentry_sdk


__version__ = '2.4.0'


def wrap(dist, group, name, sentry_dsn, timeout=None):
    """ Loads a setuptools entrypoint. If it raises an exception, forwards it
    to sentry.
    """
    sentry_sdk.init(sentry_dsn)
    entrypoint = pkg_resources.load_entry_point(dist, group, name)

    def timeout_handler(signum, frame):
        """ Called if `timeout` is set and reached.
        """
        raise TimeoutError(
            'The entrypoint wrapped by sentry-wrapper took more than '
            ' %s seconds to stop' % timeout
        )

    if timeout:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

    try:
        return entrypoint()
    except Exception as exc:  # noqa
        sentry_sdk.capture_exception(exc)
        return 1


def execute():
    """ sentry-wrapper entrypoint.
    """
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] [-- entrypoint options]',
        epilog=('Example: '
                'sentry-wrapper --dsn https://... entrypoint -- -o myarg')
    )

    parser.add_argument(
        'name',
        help='Entry point name (eg. my-entrypoint)'
    )
    parser.add_argument(
        'dist', nargs='?',
        help='Distribution name (eg. my-project==1.2.4, default: same value '
             'than name)'
    )
    parser.add_argument(
        'group', nargs='?', default='console_scripts',
        help='Entry point group (default: console_scripts)'
    )
    parser.add_argument(
        '--dsn', metavar='SENTRY_DSN', default=os.getenv('SENTRY_DSN'),
        help='Sentry DSN'
    )
    parser.add_argument(
        '-t', '--timeout', metavar='timeout',
        type=int,
        help='Timeout. After this value, TimeoutError is raised to Sentry.'
    )

    # The arguments before the double dash are the wrapper arguments. Those
    # after are the entrypoint arguments.
    try:
        rest_idx = sys.argv.index('--')
        wrapper_args = sys.argv[1:rest_idx]
        entrypoint_args = sys.argv[rest_idx + 1:]
    except ValueError:
        wrapper_args = sys.argv[1:]
        entrypoint_args = []

    args = parser.parse_args(wrapper_args)

    if args.dist is None:
        args.dist = args.name

    if args.dsn is None:
        parser.error('You must provide sentry DSN from the commandline '
                     'argument --dsn or from the environment variable '
                     'SENTRY_DSN')

    # Update sys.argv to specify the entrypoint arguments.
    old_argv = sys.argv
    sys.argv = [args.name] + entrypoint_args

    ret = wrap(args.dist, args.group, args.name, args.dsn,
               timeout=args.timeout)

    # Let's avoid to fuck up a global state.
    sys.argv = old_argv

    return ret
