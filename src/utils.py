"i21y - Locale String"

from __future__ import annotations

from typing import TypeVar, Any, overload


__all__ = ("locale_str",)


SelfT = TypeVar("SelfT", bound="locale_str")
AdtnlClsT = TypeVar("AdtnlClsT", bound="locale_str")
class locale_str:
    def __init__(self, key: Any, **extras: Any) -> None:
        self.key, self.extras = key, extras

    def _adjust_key(self, key: str) -> str:
        if not self.key.endswith("."):
            key = f".{key}"
        return key

    @overload
    def join(
        self: SelfT, *other: str | locale_str,
        cls: type[AdtnlClsT] = ...
    ) -> AdtnlClsT: ...
    def join(
        self: SelfT, *other: str | locale_str,
        cls: None = None
    ) -> SelfT: ...
    def join(
        self: SelfT, *other: str | locale_str,
        cls: type[AdtnlClsT] | None = None
    ) -> SelfT | AdtnlClsT:
        cls = cls or self.__class__
        return cls(f"{self}{self._adjust_key(str(other))}")

    def __truediv__(self: SelfT, another: str | locale_str) -> SelfT:
        return 

    def __floordiv__(self, other: str) -> str:
        return f"{self}{self._adjust_key(other)}"

    def __str__(self) -> str:
        return self.key