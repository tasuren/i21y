__all__ = ("Loader",)

from typing import TypeVar, overload

from abc import ABC, abstractmethod

from .utils import Undefined


SearchT = TypeVar("SearchT")


class Loader(ABC):
    "Abstract specification class for the class used to search Translations."

    @abstractmethod
    def search_impl(
        self, locale: str, key: str, default: SearchT | type[Undefined] = Undefined
    ) -> str | SearchT:
        "Implementation of :meth:`.abc.Loader.search`. Arguments is same as ``.search``."

    @overload
    def search(
        self, locale: str, key: str, default: type[Undefined] = Undefined
    ) -> str: ...

    @overload
    def search(
        self, locale: str, key: str, default: SearchT = Undefined
    ) -> SearchT: ...

    def search(
        self, locale: str, key: str, default: SearchT | type[Undefined] = Undefined
    ) -> str | SearchT:
        """Search translations.

        Args:
            locale: The locale of translations.
            key: The key to translations.
            default: If it is specified, it will be returned when translation is not found.

        Raises:
            TranslationNotFound: If translation is not found, this function will raise it.
        """
        return self.search_impl(locale, key, default)
