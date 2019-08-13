import sys
import os

from .constants import ENV_NAME
from .resolvers import FileResolver, EnvVarResolver


def run():
    resolver = EnvVarResolver(ENV_NAME, next_resolver=FileResolver(os.getcwd()))

    if len(sys.argv) < 2:
        for alias, path in resolver.items():
            print(alias, path, sep=' -> ')
        sys.exit()

    arg = sys.argv[1]
    if arg == "--aliases":
        for alias, _ in resolver.items():
            print(alias)
    else:
        try:
            print(resolver[arg])
        except KeyError as e:
            sys.exit("goto: Can't find bookmark {0}".format(str(e)))
