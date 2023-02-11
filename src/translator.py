"i21y - Translator"

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .loader import Loader


class Translator:
    def __init__(self, loader: Loader, default_locale: str = "en") -> None:
        self.loader, self.default_locale = loader, default_locale

    def format_(self, text: str, *args: Any, **kwargs: Any) -> str:
        return text.format(*args, **kwargs)

    def __call__(
        self, key: str, *args: Any,
        locale: str | None = None,
        **kwargs: Any
    ) -> str:
        return self.format_(self.loader.load(
            locale or self.default_locale, key
        ), *args, **kwargs)