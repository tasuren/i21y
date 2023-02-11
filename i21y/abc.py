"i21y - Loader"

__all__ = ("Loader",)

from typing import TypeVar, overload

from abc import ABC, abstractmethod

from .utils import Undefined


SearchT = TypeVar("SearchT")
class Loader(ABC):
    @abstractmethod
    def search_impl(
        self, locale: str, key: str,
        default: SearchT | type[Undefined] = Undefined
    ) -> str | SearchT: ...

    @overload
    def search(
        self, locale: str, key: str,
        default: type[Undefined] = Undefined
    ) -> str: ...
    @overload
    def search(
        self, locale: str, key: str,
        default: SearchT = Undefined
    ) -> SearchT: ...
    def search(
        self, locale: str, key: str,
        default: SearchT | type[Undefined] = Undefined
    ) -> str | SearchT:
        return self.search_impl(locale, key, default)