import argparse
import os
import signal
import sys

import pkg_resources

import sentry_sdk


__version__ = '2.5.1'


class SentryConfig(object):
    def __init__(
        self,
        dsn,
        release=None,
        environment=None,
        server_name=None,
        attach_stacktrace=None,
        include_local_variables=None,
    ):
        self.dsn = dsn
        self.release = release
        self.environment = environment
        self.server_name = server_name
        self.attach_stacktrace = attach_stacktrace
        self.include_local_variables = include_local_variables

        self._conf_values = {"dsn": self.dsn}
        if self.release is not None:
            self._conf_values["release"] = self.release
        if self.environment is not None:
            self._conf_values["environment"] = self.environment
        if self.server_name is not None:
            self._conf_values["server_name"] = self.server_name
        if self.attach_stacktrace is not None:
            self._conf_values["attach_stacktrace"] = self.attach_stacktrace
        if self.include_local_variables is not None:
            self._conf_values["include_local_variables"] = self.include_local_variables

    def keys(self):
        return self._conf_values.keys()

    def __getitem__(self, key):
        return self._conf_values[key]


def wrap(dist, group, name, sentry_config, timeout=None):
    """ Loads a setuptools entrypoint. If it raises an exception, forwards it
    to sentry.
    """
    sentry_sdk.init(**sentry_config)
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
        '-t', '--timeout', metavar='timeout',
        type=int,
        help='Timeout. After this value, TimeoutError is raised to Sentry.'
    )
    parser.add_argument(
        '--dsn', metavar='SENTRY_DSN', default=os.getenv('SENTRY_DSN'),
        help='Sentry DSN',
    )
    parser.add_argument(
        '--release',
        nargs='?',
        help="The program's release version (e.g. 3.2.3)",
    )
    parser.add_argument(
        '--environment',
        nargs='?',
        help='The envionment the program is running in (e.g. staging)',
    )
    parser.add_argument(
        '--server-name',
        nargs='?',
        help='The name of the server the program is running on'
    )
    parser.add_argument(
        '--attach-stacktrace',
        action="store_const",
        const=True,
        help='Attach stacktrace to each sent message'
    )
    parser.add_argument(
        '--include-local-variables',
        action="store_const",
        const=True,
        help='Send local variables along with stackframes'
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

    sentry_config = SentryConfig(
        args.dsn,
        args.release,
        args.environment,
        args.server_name,
        args.attach_stacktrace,
        args.include_local_variables,
    )

    # Update sys.argv to specify the entrypoint arguments.
    old_argv = sys.argv
    sys.argv = [args.name] + entrypoint_args

    ret = wrap(args.dist, args.group, args.name, sentry_config,
               timeout=args.timeout)

    # Let's avoid to fuck up a global state.
    sys.argv = old_argv

    return ret
