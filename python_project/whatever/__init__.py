import sys
import time


def ok(*args, **kwargs):
    print ('Entrypoint ok called with', args, kwargs)

def exception(*args, **kwargs):
    print ('Entrypoint "exception" called with', args, kwargs)
    raise ValueError

def timeout(*args, **kwargs):
    print ('Entrypoint "timeout" called with', args, kwargs)
    while True:
        print ('.')
        time.sleep(1)
