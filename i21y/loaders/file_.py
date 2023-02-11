"i21y Loaders - File"

from __future__ import annotations

__all__ = ("LocaleFile", "Loader")

from typing import NamedTuple, TypeAlias, cast
from collections.abc import Iterable

from collections import defaultdict
from functools import cache

from pathlib import PurePath
from os.path import exists, isfile
from os import walk

from ..abc import Loader as AbcLoader, SearchT
from ..error import TextNotFound
from ..utils import Undefined


DataDict: TypeAlias = dict[str, "str | DataDict"]
class LocaleFile:
    def __init__(self, parent: Loader, locale: str, path: PurePath) -> None:
        self.parent, self.path, self.data = parent, path, DataDict()
        self.locale, self.key = locale, ".".join(
            self.path.parts[parent.path_size+1:-1]
            + (self.path.stem,)
        )

    def get(self, key: str | Iterable[str]) -> str | None:
        if isinstance(key, str):
            key = key.split(".")
        tentative, result = None, None
        for partial in key:
            if result is not None:
                # なぜ下の`result = ...`ではなくここでわざわざ`return`するかは、既に文字列まで辿り着いたのに深くまでいくということがないようにするためのもの。
                # 例えば、`a.b.c`で文字列があるとき、`a.b.c.d.e`のeまでアクセスがすることができてしまう。
                # ましてや、`a.b.c`の文字列が返却される。これはよろしくないので、わざと一度イテレートしてからreturnをして、呼び出し元にエラーを認識してもらう。
                return
            try:
                if tentative is None:
                    tentative = self.data[partial]
                else:
                    assert not isinstance(tentative, str)
                    tentative = tentative[partial]
                if isinstance(tentative, str):
                    result = tentative
            except KeyError:
                break
        if result is not None:
            return result

    def __str__(self) -> str:
        return f"<LocaleFile path={self.path}>"


class Caches(NamedTuple):
    text: defaultdict[str, dict[str, LocaleFile]]
    key_mapping: dict[tuple[str, str], tuple[str, list[str]]]

    def clear(self) -> None:
        self.text.clear()
        self.key_mapping.clear()

    def __str__(self) -> str:
        return f"<Caches text={self.text} key_mapping={self.key_mapping}>"


class Loader(AbcLoader):

    EXTENSIONS = tuple[str, ...]()

    def __init__(
        self, path: str | PurePath,
        preload_cache: bool = True,
        use_cache_realtime: bool = True,
        do_not_search_file: bool = False,
        primary_extension_index: int = 0
    ) -> None:
        if isinstance(path, str):
            path = PurePath(path)
        self.path = path
        self.path_size = len(path.parts)
        self.primary_extension_index = primary_extension_index
        self.do_not_search_file = do_not_search_file

        self.caches = Caches(defaultdict(dict), {})

        self.use_cache_realtime = use_cache_realtime
        if preload_cache:
            self.make_cache()

        if not self.EXTENSIONS:
            raise NotImplementedError("The file extension is not set. This indicates that this class is not properly implemented.")

    def load(self, path: PurePath) -> LocaleFile:
        return LocaleFile(self, path.parts[self.path_size], path)

    def make_cache(self) -> None:
        for root, _, files in walk(self.path):
            for file_name in files:
                if not file_name.endswith(self.EXTENSIONS):
                    continue
                lf = self.load(PurePath(root).joinpath(file_name))
                self.caches.text[lf.locale][lf.key] = lf

    @cache
    def get_locale_path(self, locale: str) -> PurePath:
        return self.path.joinpath(locale)

    @property
    def primary_extension(self) -> str:
        return self.EXTENSIONS[self.primary_extension_index]

    def add_extension(self, file_name: str) -> str:
        return f"{file_name}{self.primary_extension}"

    def search_locale_file(self, locale: str, key: str) -> tuple[list[str], LocaleFile] | None:
        # キャッシュを検索する。
        if self.use_cache_realtime:
            # 指定されたキーの文章たあるファイルのキーがキーマッピングのキャッシュにあるかを検索する。
            if (locale, key) in self.caches.key_mapping:
                file_key, end_of_key = self.caches.key_mapping[(locale, key)]
                return end_of_key, self.caches.text[locale][file_key]

            # 普通に指定されたキーのファイルをキャッシュから検索する。
            for tentative in filter(key.startswith, self.caches.text[locale].keys()):
                end_of_key = key.replace(tentative, "")
                if end_of_key.startswith("."):
                    end_of_key = end_of_key[1:]
                _, eok = self.caches.key_mapping[(locale, key)] \
                    = (tentative, end_of_key.split("."))
                return eok, self.caches.text[locale][tentative]

        if self.do_not_search_file:
            return

        # 検索を行う。
        path, file_key = self.get_locale_path(locale), ""
        for index, partial in enumerate(keys := key.split(".")):
            file_key += f"{partial}."

            # ディレクトリかどうかをチェックする。
            path = path.joinpath(partial)
            if exists(path):
                continue

            # ファイルかどうかをチェックする。
            for ext in self.EXTENSIONS:
                path = path.with_suffix(ext)
                if exists(path) or isfile(path):
                    # ファイルが存在したのなら、ロードを行う。
                    lf = self.load(path)
                    if self.use_cache_realtime:
                        self.caches.text[locale][file_key[:-1]] = lf
                    return keys[index+1:], lf
            else:
                break

    _TNF_T = "Not found text: %s"
    def search_impl(
        self, locale: str, key: str,
        default: type[Undefined] | SearchT = Undefined
    ) -> str | SearchT:
        result = self.search_locale_file(locale, key)
        if result is None:
            if default is Undefined:
                raise TextNotFound(key, self._TNF_T % key)
            return cast(SearchT, default)
        end_of_key, lf = result
        if (text := lf.get(end_of_key)) is None:
            raise TextNotFound(key, self._TNF_T % key)
        return text