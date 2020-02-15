import os

from gotofolder.helpers import home_dir, Path


TESTDATA_DIR = "testdata"


class MockHasParentPath(Path):
    def has_parent(self):
        return self.realpath() != os.path.abspath(TESTDATA_DIR)


class TestPath:
    def test_realpath_is_abs_path(self):
        p = Path(TESTDATA_DIR)

        assert os.path.isabs(p.realpath())
        assert p.realpath() == os.path.abspath(TESTDATA_DIR)

    def test_path_with_parent(self):
        p = MockHasParentPath(TESTDATA_DIR + "/a")

        assert p.has_parent()
        assert p.parent().realpath() == os.path.abspath(TESTDATA_DIR)

    def test_path_without_parent(self):
        p = MockHasParentPath(TESTDATA_DIR)

        assert p.has_parent() is False
        assert p.parent() == p

    def test_the_actual_root(self):
        p = Path(home_dir())

        assert p.has_parent() is False

    def test_get_child(self):
        p = Path(TESTDATA_DIR)

        # Direct child
        assert p.get_child("a").realpath() == os.path.abspath(TESTDATA_DIR + "/a")

        # Child of a child of a child
        assert p.get_child("a").get_child("b").get_child("c").realpath() == os.path.abspath(TESTDATA_DIR + "/a/b/c")

        # Parent of a child
        assert p.get_child("a").parent().realpath() == p.realpath()

    def test_is_file(self):
        p = Path(TESTDATA_DIR)

        assert p.get_child(".goto").is_file()
        assert not p.get_child("a").is_file()
