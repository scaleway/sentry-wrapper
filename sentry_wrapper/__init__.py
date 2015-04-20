import argparse
import os
import sys

import pkg_resources

import raven


__version__ = '1.0.0'


def wrap(dist, group, name, sentry_dsn):
    """ Loads a setuptools entrypoint. If it raises an exception, forwards it
    to sentry.
    """
    sentry_client = raven.Client(sentry_dsn)
    entrypoint = pkg_resources.load_entry_point(dist, group, name)

    try:
        return entrypoint()
    except:
        sentry_client.captureException()
        return 1


def execute():
    """ sentry-wrapper entrypoint.
    """
    parser = argparse.ArgumentParser()

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

    args = parser.parse_args()

    if args.dist is None:
        args.dist = args.name

    if args.dsn is None:
        parser.error('You must provide sentry DSN from the commandline '
                     'argument --dsn or from the environment variable '
                     'SENTRY_DSN')

    return wrap(args.dist, args.group, args.name, args.dsn)
