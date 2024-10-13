__all__ = ("Loader",)

from pathlib import PurePath

try:
    from yaml import load

    try:
        from yaml import CLoader as YamlLoader
    except ImportError:
        from yaml import Loader as YamlLoader
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "pyyaml is not installed. Please install `pyyaml` or `i21y[yaml]` by pip: %s"
        % e
    )

from .file_ import Loader as FileLoader
from .file_ import LocaleFile


class Loader(FileLoader):
    """Loader implemented to load YAML files.
    To use it, you must have ``pyyaml`` or ``i21y[yaml]`` installed.
    The arguments of constructor are same as :class:`.file_.Loader`."""

    EXTENSIONS = (".yml", ".yaml")

    def load(self, path: PurePath) -> LocaleFile:
        lf = super().load(path)
        with open(lf.path, "rb") as f:
            lf.data = load(f, YamlLoader)
        return lf
