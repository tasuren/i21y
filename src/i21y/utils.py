from __future__ import annotations

__all__ = ("Undefined", "locale_str")

from typing import TypeAlias, TypeVar, Any, overload
from collections.abc import Iterable


class Undefined:
    "This class is used to represent undefined."


LocaleStr: TypeAlias = "str | locale_str"
SelfT = TypeVar("SelfT", bound="locale_str")
AdtnlClsT = TypeVar("AdtnlClsT", bound="locale_str")


class locale_str:
    """This class is designed to allow for the graceful creation of keys to translations.

    **Operations**

    .. describe:: x + y

        It is alias for :meth:`locale_str.join`.
        y can be specified str or Iterable, and y will be passed to :meth:`.join` as arguments.
    .. describe:: x & y

        It is alias for :meth:`locale_str.join_raw`.
        y can be specified str or Iterable, and y will be passed to :meth:`.join_raw` as arguments.
    .. describe:: x == y

        Checks if :attr:`locale_str.key` of x and y are the same.
    .. describe:: x != y

        Checks if :attr:`locale_str.key` of x and y are not the same.

    Args:
        key: The key to ranslation.
        **extras: It is for some data.

    Notes:
        Attribute can be used as the argument of :meth:`.join`."""

    def __init__(self, key: Any, **extras: Any) -> None:
        self.key, self.extras = key, extras

    def _adjust_key(self, key: str) -> str:
        if not self.key.endswith("."):
            key = f".{key}"
        return key

    def join_raw(self, *other: str | locale_str) -> str:
        """Concatenate strings to self and return string of it.

        Args:
            *other: Target strings."""
        new = self.key
        for partial in other:
            if not isinstance(partial, str):
                partial = str(partial)
            new = f"{new}{self._adjust_key(partial)}"
        return new

    @overload
    def join(
        self: ..., *other: str | locale_str, cls: type[AdtnlClsT], **extras: Any
    ) -> AdtnlClsT: ...

    @overload
    def join(
        self: SelfT, *other: str | locale_str, cls: None = None, **extras: Any
    ) -> SelfT: ...

    def join(
        self: SelfT,
        *other: str | locale_str,
        cls: type[AdtnlClsT] | None = None,
        **extras: Any,
    ) -> SelfT | AdtnlClsT:
        """A version of :meth:`locale_str.join_raw` that returns the instance of the class that self.

        Args:
            *other: Target strings.
            cls: The :class:`.locale_str` used to create the instance.
            **extras: The value to pass to the ``extras`` argument of the constructor of :class:`.locale_str`.
        """
        cls = cls or self.__class__  # type: ignore
        assert cls is not None
        return cls(self.join_raw(*other), **extras)

    def update_extras(self: SelfT, **extras: Any) -> SelfT:
        """Function to gracefully update :attr:`.extras`.

        Args:
            extras: The extras to override."""
        self.extras.update(**extras)
        return self

    def __add__(self: SelfT, other: LocaleStr | Iterable[LocaleStr]) -> SelfT:
        if isinstance(other, str | locale_str):
            other = (other,)
        return self.join(*other)

    def __and__(self, other: str | Iterable[str]) -> str:
        if isinstance(other, str):
            other = (other,)
        return self.join_raw(*other)

    def __getattr__(self: SelfT, another: str) -> SelfT:
        return self.join(another)

    def __eq__(self, another: locale_str) -> bool:
        return self.key == another.key

    def __ne__(self, another: locale_str) -> bool:
        return self.key != another.key

    def __str__(self) -> str:
        return self.key
