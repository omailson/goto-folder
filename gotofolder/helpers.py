import os


def home_dir():
    return os.path.expanduser('~')


def get_expanded_path(path):
    # Expand environment vars
    path = os.path.expandvars(path)

    # Expand user var (eg: ~)
    path = os.path.expanduser(path)

    return path


class Path:
    def __init__(self, path: str):
        self._realpath = os.path.abspath(path)

    def realpath(self) -> str:
        return self._realpath

    def has_parent(self):
        return self._realpath != home_dir()

    def parent(self) -> 'Path':
        if not self.has_parent():
            return self

        return Path(os.path.dirname(self._realpath))

    def get_child(self, child_path: str) -> 'Path':
        expanded_path = get_expanded_path(child_path)
        path_with_base = os.path.join(self._realpath, expanded_path)
        return Path(path_with_base)

    def is_file(self):
        return os.path.isfile(self._realpath)

    def __str__(self):
        return self.realpath()
