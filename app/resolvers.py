import os

from .constants import SEPARATOR, GOTO_FILE_NAME
from .helpers import is_root


# BaseResolver class. Should be used as a base class to any resolver
class BaseResolver:
    def __init__(self, next_resolver=None):
        self.__next_resolver = next_resolver
        self.__resolved_paths = None

    @property
    def next(self):
        if self.__next_resolver is not None:
            return self.__next_resolver

        next_resolver = self.next_resolver()
        if next_resolver is not None:
            return next_resolver

        # Return an empty dict so it can raise a KeyError for any key
        return {}

    def next_resolver(self):
        return None

    def __getitem__(self, key):
        path = self.__get_resolved_paths().get(key)
        if path is not None:
            return path

        return self.next[key]

    def __get_resolved_paths(self):
        if self.__resolved_paths is None:
            self.__resolved_paths = self.resolve()
        return self.__resolved_paths

    def items(self):
        resolved_paths = self.__get_resolved_paths().copy()

        for alias, path in self.next.items():
            if alias not in resolved_paths:
                resolved_paths[alias] = path

        return resolved_paths.items()


# A resolver that has no keys and no next_resolver
class RootResolver(BaseResolver):
    def resolve(self):
        return {}


class FileResolver(BaseResolver):
    def __init__(self, path, *args, **kwargs):
        self.__path = path
        super(FileResolver, self).__init__(*args, **kwargs)

    @property
    def path(self):
        return self.__path

    def resolve(self):
        goto_file = os.path.abspath(os.path.join(self.path, GOTO_FILE_NAME))
        if not os.path.isfile(goto_file):
            return {}

        resolved = {}
        with open(goto_file, 'r') as f:
            bookmarks = f.read().splitlines()

            for b in bookmarks:
                alias, path = b.split(SEPARATOR)
                resolved[alias] = os.path.abspath(os.path.join(self.path, path))

        return resolved

    def next_resolver(self):
        if is_root(self.path):
            return RootResolver()

        return FileResolver(os.path.dirname(self.path))

    def __repr__(self):
        return "FileResolver({0})".format(self.path)


class EnvVarResolver(BaseResolver):
    DEFAULT_SEPARATOR = ','

    def __init__(self, envname, sep=DEFAULT_SEPARATOR, *args, **kwargs):
        super(EnvVarResolver, self).__init__(*args, **kwargs)
        self.__envname = envname
        self.sep = sep

    @property
    def envname(self):
        return self.__envname

    def resolve(self):
        gotofolders = os.getenv(self.envname)
        if not gotofolders:
            return {}

        resolved_paths = {}
        bookmarks = gotofolders.split(self.sep)
        for b in bookmarks:
            if not b:
                continue

            alias, path = b.split(SEPARATOR)
            if not alias or not path:
                continue
            if not os.path.isabs(path):
                continue

            resolved_paths[alias] = path

        return resolved_paths

    def __repr__(self):
        return "EnvVarResolver(${0})".format(self.envname)
