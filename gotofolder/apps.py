import sys
import os

from .constants import ENV_NAME
from .resolvers import FileResolver, EnvVarResolver


def create_resolver():
    return EnvVarResolver(ENV_NAME, next_resolver=FileResolver(os.getcwd()))


def run():
    resolver = create_resolver()

    if len(sys.argv) < 2:
        for alias, path in resolver.items():
            print(alias, path, sep=' -> ')
        sys.exit()

    key = sys.argv[1]
    try:
        print(resolver[key])
    except KeyError as e:
        sys.exit("goto: Can't find bookmark {0}".format(str(e)))


def aliases():
    resolver = create_resolver()
    for alias, _ in resolver.items():
        print(alias)
