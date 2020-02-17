import os

from gotofolder.helpers import Path
from gotofolder.resolvers import FileResolver, EnvVarResolver, DictResolver, BaseResolver

TESTDATA_DIR = "testdata"
TESTENVVAR = "MOCK_GOTOFOLDERS"


class MockPath(Path):
    def has_parent(self):
        return self.realpath() != os.path.abspath(TESTDATA_DIR)


def create_resolver_in(path=None):
    cwd = MockPath(TESTDATA_DIR)
    if path is not None:
        cwd = cwd.get_child(path)

    return EnvVarResolver(TESTENVVAR, next_resolver=FileResolver(cwd))


def path_to(path):
    return os.path.abspath(os.path.join(TESTDATA_DIR, path))


def assert_key_error(resolver: BaseResolver, key: str):
    try:
        _ = resolver[key]
        assert False
    except KeyError:
        assert True


class TestResolvers:
    # Test base resolver
    def test_unknown_bookmark(self):
        resolver = create_resolver_in()

        assert_key_error(resolver, "x")

    def test_slashes_are_ignored(self):
        resolver = create_resolver_in()

        assert_key_error(resolver, "a/c")

    def test_dots_are_ignored(self):
        key = "foo.bar"
        resolver = DictResolver({key: "bar"})

        assert_key_error(resolver, key)

    # Test file resolver
    def test_simple_resolve(self):
        resolver = create_resolver_in()

        expected_path = path_to("a")
        path_to_a = resolver["a"]
        assert path_to_a == expected_path

        expected_path2 = path_to("a/b/c")
        path_to_abc = resolver["abc"]
        assert path_to_abc == expected_path2

    def test_resolve_in_subfolder(self):
        resolver = create_resolver_in("a")

        path_to_aa = path_to("a/a")
        path_to_a = path_to("a")
        path_to_abc = path_to("a/b/c")

        # Assert child overrides
        assert resolver["a"] == path_to_aa

        # Assert relative path
        assert resolver["aa"] == path_to_a

        # Assert subfolder
        assert resolver["bc"] == path_to_abc

        # Assert use of parent .goto
        assert resolver["abc"] == path_to_abc

    # Test envvar resolver
    def test_envvarresolver_pass_to_the_next_resolver(self):
        resolver = EnvVarResolver(TESTENVVAR, next_resolver=DictResolver({"foo": "bar"}))

        assert resolver["foo"] == "bar"
