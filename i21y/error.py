"i21y - Error"

__all__ = ("I21YError", "TextNotFound")

from typing import Any


class I21YError(Exception):
    pass

class TextNotFound(I21YError):
    def __init__(self, key: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.key = key