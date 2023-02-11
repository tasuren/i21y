"i21y Loaders - Json"

__all__ = ("Loader",)

from pathlib import PurePath

from .file_ import Loader as FileLoader, LocaleFile

try:
    from orjson import loads
except ModuleNotFoundError:
    from json import loads


class Loader(FileLoader):

    EXTENSIONS = (".json",)

    def load(self, path: PurePath) -> LocaleFile:
        lf = super().load(path)
        with open(lf.path, "rb") as f:
            lf.data = loads(f.read())
        return lf