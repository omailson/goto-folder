import os


def home_dir():
    return os.path.expanduser('~')


def is_root(path):
    return path == home_dir()
