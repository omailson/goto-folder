import os

from .constants import SEPARATOR, GOTO_FILE_NAME
from .helpers import Path


# BaseResolver class. Should be used as a base class to any resolver
class BaseResolver:
    def __init__(self, *args, **kwargs):
        self.__resolved_paths = None

    @property
    def next(self):
        next_resolver = self.next_resolver()
        if next_resolver is not None:
            return next_resolver

        # Return an empty dict so it can raise a KeyError for any key
        return {}

    def next_resolver(self):
        return None

    def __getitem__(self, key) -> str:
        path = self.__get_resolved_paths().get(key)
        if path is not None:
            return str(path)

        return self.next[key]

    def __get_resolved_paths(self):
        if self.__resolved_paths is None:
            self.__resolved_paths = self.resolve()
            # Remove bookmarks with forbidden characters
            self.__resolved_paths = {k: v for k, v in self.__resolved_paths.items() if '.' not in k and '/' not in k}
        return self.__resolved_paths

    def items(self):
        resolved_paths = self.__get_resolved_paths().copy()

        for alias, path in self.next.items():
            if alias not in resolved_paths:
                resolved_paths[alias] = path

        return resolved_paths.items()

    def resolve(self):
        raise NotImplementedError


# A resolver that resolves to the keys of a given dictionary
class DictResolver(BaseResolver):
    def __init__(self, d, *args, **kwargs):
        self._d = d
        super(DictResolver, self).__init__(*args, **kwargs)

    def resolve(self):
        return self._d


class FileResolver(BaseResolver):
    def __init__(self, path: Path, *args, **kwargs):
        self.__path = path
        super(FileResolver, self).__init__(*args, **kwargs)

    @property
    def path(self):
        return self.__path

    def resolve(self):
        goto_file = self.__goto_file_path()
        if not goto_file.is_file():
            return {}

        resolved = {}
        with open(goto_file.realpath(), 'r') as f:
            bookmarks = f.read().splitlines()

            for b in bookmarks:
                alias, path = b.split(SEPARATOR)
                resolved[alias] = self.path.get_child(path)

        return resolved

    def next_resolver(self):
        if not self.path.has_parent():
            return None

        return FileResolver(self.path.parent())

    def __goto_file_path(self):
        return self.path.get_child(GOTO_FILE_NAME)

    def __repr__(self):
        return "FileResolver({0})".format(self.__goto_file_path())


class EnvVarResolver(BaseResolver):
    DEFAULT_SEPARATOR = ','

    def __init__(self, envname, sep=DEFAULT_SEPARATOR, next_resolver=None, *args, **kwargs):
        super(EnvVarResolver, self).__init__(*args, **kwargs)
        self.__envname = envname
        self._next_resolver = next_resolver
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

            resolved_paths[alias] = Path(path)

        return resolved_paths

    def next_resolver(self):
        return self._next_resolver

    def __repr__(self):
        return "EnvVarResolver(${0})".format(self.envname)
