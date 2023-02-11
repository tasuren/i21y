"i21y - Loader"

from abc import ABC, abstractmethod


__all__ = ("Loader",)


class Loader(ABC):
    @abstractmethod
    def load(self, locale: str, key: str) -> str:
        ...