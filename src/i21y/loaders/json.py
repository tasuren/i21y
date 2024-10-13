__all__ = ("Loader",)

from pathlib import PurePath

from .file_ import Loader as FileLoader
from .file_ import LocaleFile

try:
    from orjson import loads
except ModuleNotFoundError:
    from json import loads


class Loader(FileLoader):
    """Loader implemented to load json files.
    By default, json is read using the standard module json.
    But if you have ``orjson`` or ``i21y[fast-json]`` installed, json reading is done with the library called orjson.
    The arguments of constructor are same as :class:`.file_.Loader`."""

    EXTENSIONS = (".json",)

    def load(self, path: PurePath) -> LocaleFile:
        lf = super().load(path)
        with open(lf.path, "rb") as f:
            lf.data = loads(f.read())
        return lf
