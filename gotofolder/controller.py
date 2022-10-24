from typing import Sequence

from gotofolder.helpers import Path
from gotofolder.resolvers import ResolvedPath, EnvVarResolver, FileResolver


class Resolver:
    def items(self) -> Sequence[ResolvedPath]: ...


class Controller:
    def __init__(self, cwd: Path, envvar: str):
        self.cwd = cwd
        self.envvar = envvar

    def resolve_alias(self, alias: str) -> ResolvedPath:
        keys = alias.split('.')
        cwd = self.cwd
        resolved_path = None
        for k in keys:
            resolved_path = self._resolve_single_alias(cwd, k)
            cwd = resolved_path.path

        return resolved_path

    def _resolve_single_alias(self, cwd: Path, alias: str) -> ResolvedPath:
        # First, try to get a value from the env var
        envvar_resolver = EnvVarResolver(self.envvar, EnvVarResolver.DEFAULT_SEPARATOR)
        resolved_path = envvar_resolver.get(alias)
        if resolved_path is not None:
            return resolved_path

        # If not found, try to find the alias in `cwd` or in its ascendants
        path = cwd
        while path.has_parent():
            file_resolver = FileResolver(path)
            resolved_path = file_resolver.get(alias)
            if resolved_path is not None:
                return resolved_path
            path = path.parent()

        raise KeyError

    def _list_multikey_aliases(self, prefix: str = ''):
        resolved_paths = []
        envvar_resolver = EnvVarResolver(self.envvar, EnvVarResolver.DEFAULT_SEPARATOR)
        resolved_paths.extend(envvar_resolver.resolved_items())

        keys = prefix.split('.')
        cwd = self.cwd
        resolved_path = None
        for k in keys:
            resolved_path = self._resolve_single_alias(cwd, k)
            cwd = resolved_path.path

    def _list_single_alias(self, cwd: Path) -> Sequence[ResolvedPath]:
        resolved_paths = []

        path = cwd
        while path.has_parent():
            file_resolver = FileResolver(path)
            resolved_paths.extend(file_resolver.resolved_items())
            path = path.parent()

        return resolved_paths
