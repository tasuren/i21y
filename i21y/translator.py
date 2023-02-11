"i21y - Translator"

from __future__ import annotations

__all__ = ("Translator",)

from typing import TYPE_CHECKING, TypeVar, Generic, Any

if TYPE_CHECKING:
    from .abc import Loader
    from .utils import locale_str


LoaderT = TypeVar("LoaderT", bound="Loader")
class Translator(Generic[LoaderT]):
    def __init__(self, loader: LoaderT | Loader, default_locale: str = "en") -> None:
        self.loader, self.default_locale = loader, default_locale

    def format_(self, text: str, *args: Any, **kwargs: Any) -> str:
        return text.format(*args, **kwargs)

    def translate(self, key: str | locale_str, *args: Any, **kwargs: Any) -> str:
        return self(key, *args, **kwargs)

    def __call__(
        self, key: str | locale_str, *args: Any,
        locale: str | None = None,
        **kwargs: Any
    ) -> str:
        return self.format_(self.loader.search(
            locale or self.default_locale,
            key if isinstance(key, str) else str(key)
        ), *args, **kwargs)