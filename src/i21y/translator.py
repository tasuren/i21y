from __future__ import annotations

__all__ = ("Translator",)

from typing import TYPE_CHECKING, TypeVar, Generic, Any, cast

if TYPE_CHECKING:
    from .abc import Loader
    from .utils import locale_str


LoaderT = TypeVar("LoaderT", bound="Loader")


class Translator(Generic[LoaderT]):
    """This class is for translation.

    Args:
        loader: It is for searching translations.
        default_locale: It will be used for default locale. If you don't specify it, it will be set `en`.
    """

    def __init__(self, loader: LoaderT | Loader, default_locale: str = "en") -> None:
        self.loader: LoaderT = cast(LoaderT, loader)
        self.default_locale = default_locale

    def format_(self, text: str, *args: Any, **kwargs: Any) -> str:
        """Format text.

        Args:
            text: Target text.
            *args: The arguments to be passed to ``text.format``.
            **kwargs: The keyword arguments to be passed to ``text.format``."""
        return (
            text.format(*args, **kwargs)
            if kwargs.pop("__i21y_special_kwarg_do_format", True)
            else text
        )

    def translate(
        self,
        key: str | locale_str,
        *args: Any,
        locale: str | None = None,
        do_format: bool = True,
        **kwargs: Any,
    ) -> str:
        """Do translation.
        The translation will be formated by :meth:`Translator.format_`.

        Args:
            key: It will be used for searching text.
            *args: The arguments to be passed to :meth:`.format_`.
            locale: The locale of text.
            do_format: Whether or not to perform formatting.
            **kwargs: The arguments to be passed to :meth:`.format_`.

        Note:
            It can be called by calling instance of :class:`Translator`. Like:

            .. code-block:: python

                t = Translator()
                print(t("responses.not_found"))

        Raises:
            TranslationNotFound: If translation is not found, this function will raise it.
        """
        kwargs["__i21y_special_kwarg_do_format"] = do_format
        return self.format_(
            self.loader.search(
                locale or self.default_locale, key if isinstance(key, str) else str(key)
            ),
            *args,
            **kwargs,
        )

    def __call__(self, key: str | locale_str, *args: Any, **kwargs: Any) -> str:
        return self.translate(key, *args, **kwargs)

    def __str__(self) -> str:
        return f"<Translator loader={self.loader} default_locale={self.default_locale}>"
