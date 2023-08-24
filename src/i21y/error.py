__all__ = ("I21YError", "TranslationNotFound")

from typing import Any


class I21YError(Exception):
    "The exception class used to throw the exception on i21y."


class TranslationNotFound(I21YError):
    """The exception class will be raised when text is not found.

    Args:
        key: The key of text.
        *args: The arguments to be passed to :class:`I21YError`.
        *kwargs: The keyword arguments to be passed to :class:`I21YError`."""

    def __init__(self, key: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.key = key
