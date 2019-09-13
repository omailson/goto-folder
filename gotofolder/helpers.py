import os


def home_dir():
    return os.path.expanduser('~')


def is_root(path):
    return path == home_dir()


def get_expanded_path(path):
    # Expand environment vars
    path = os.path.expandvars(path)

    # Expand user var (eg: ~)
    path = os.path.expanduser(path)

    return path