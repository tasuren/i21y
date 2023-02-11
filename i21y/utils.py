"i21y - Locale String"

from __future__ import annotations

from typing import TypeVar, Any, overload


__all__ = ("Undefined", "locale_str")


class Undefined:
    def __eq__(self, _) -> bool:
        return False


SelfT = TypeVar("SelfT", bound="locale_str")
AdtnlClsT = TypeVar("AdtnlClsT", bound="locale_str")
class locale_str:
    def __init__(self, key: Any, **extras: Any) -> None:
        self.key, self.extras = key, extras

    def _adjust_key(self, key: str) -> str:
        if not self.key.endswith("."):
            key = f".{key}"
        return key

    def join_raw(self, *other: str | locale_str) -> str:
        new = self.key
        for partial in other:
            if not isinstance(partial, str):
                partial = str(partial)
            new = f"{new}{self._adjust_key(partial)}"
        return new

    @overload
    def join(
        self: ..., *other: str | locale_str,
        cls: type[AdtnlClsT] = None
    ) -> AdtnlClsT: ...
    @overload
    def join(
        self: SelfT, *other: str | locale_str,
        cls: None = None
    ) -> SelfT: ...
    def join(
        self: SelfT, *other: str | locale_str,
        cls: type[AdtnlClsT] | None = None
    ) -> SelfT | AdtnlClsT:
        cls = cls or self.__class__ # type: ignore
        assert cls is not None
        return cls(self.join_raw(*other))

    def __truediv__(self: SelfT, another: str | locale_str) -> SelfT:
        return self.join(another)

    def __floordiv__(self, other: str) -> str:
        return self.join_raw(other)

    def __eq__(self, another: locale_str) -> bool:
        return self.key == another.key

    def __ne__(self, another: locale_str) -> bool:
        return self.key != another.key

    def __str__(self) -> str:
        return self.key