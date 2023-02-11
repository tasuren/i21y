"i21y Loaders - YAML"

from typing import Any

from pathlib import PurePath

try:
    from yaml import load
    try:
        from yaml import CLoader as YamlLoader
    except ImportError:
        from yaml import Loader as YamlLoader
except ModuleNotFoundError as e:
    raise ModuleNotFoundError("pyyaml is not installed. Please install `pyyaml` or `i21y[yaml]` by pip: %s" % e)

from .file_ import Loader as FileLoader, LocaleFile


class Loader(FileLoader):

    EXTENSIONS = (".yml", ".yaml")

    def load(self, path: PurePath) -> LocaleFile:
        lf = super().load(path)
        with open(lf.path, "rb") as f:
            lf.data = load(f, YamlLoader)
        return lf


class PythonI18NCompatibleLoader(FileLoader):

    EXTENSIONS = Loader.EXTENSIONS

    def __init__(
        self, *args: Any,
        replace_percent_braces: bool = True,
        **kwargs: Any
    ) -> None:
        self.replace_percent_braces = replace_percent_braces
        super().__init__(*args, **kwargs)    

    def load(self, path: PurePath) -> LocaleFile:
        lf = super().load(path)
        with open(path, "r") as f:
            raw = f.read()
        # Replace percent braces for `str.format`.
        if self.replace_percent_braces:
            raw = raw.replace("%{", "{")
        lf.data = load(raw, YamlLoader)
        return lf