import argparse
import os

import raven

__version__ = '2.2.0'


def execute():
    """ sentry-msg entrypoint.
    """
    parser = argparse.ArgumentParser(
        usage='%(prog)s [options] [message to send]',
        epilog=('Example: '
                'sentry-msg --dsn https://... "send me"')
    )

    parser.add_argument(
        'msg',
        help='Message to send'
    )
    parser.add_argument(
        '--dsn', metavar='SENTRY_DSN', default=os.getenv('SENTRY_DSN'),
        help='Sentry DSN'
    )

    args = parser.parse_args()

    if args.dsn is None:
        parser.error('You must provide sentry DSN from the commandline '
                     'argument --dsn or from the environment variable '
                     'SENTRY_DSN')

    if args.msg is None:
        parser.error('Nothing to send')

    sentry_client = raven.Client(args.dsn)
    sentry_client.captureMessage(args.msg)

    return 0
