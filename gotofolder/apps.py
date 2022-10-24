import sys
import os

from .constants import ENV_NAME
from .helpers import Path
from .resolvers import FileResolver, EnvVarResolver


def create_resolver():
    return EnvVarResolver(ENV_NAME, next_resolver=FileResolver(Path(os.getcwd())))


def run():
    resolver = create_resolver()

    if len(sys.argv) < 2:
        for alias, path in resolver.items():
            print(alias, path, sep=' -> ')
        sys.exit()

    key = sys.argv[1]
    keys = key.split('.')
    try:
        p = '.'
        for k in keys:
            p = resolver[k]
            resolver = FileResolver(Path(p))
        print(p)
    except KeyError as e:
        sys.exit("goto: Can't find bookmark {0}".format(str(e)))


def aliases():
    resolver = create_resolver()
    for alias, _ in resolver.items():
        print(alias)
