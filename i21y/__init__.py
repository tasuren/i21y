"tasuren - i21y"

__author__ = "Takagi Tasuku"
__version__ = "0.1.0a0"
__all__ = ("Translator", "I21YError", "TextNotFound", "locale_str")

from .translator import Translator
from .error import I21YError, TextNotFound
from .utils import locale_str