"tasuren - i21y"

__author__ = "Takagi Tasuku"
__version__ = "0.1.0b2"
__all__ = ("Translator", "I21YError", "TranslationNotFound", "locale_str")

from .translator import Translator
from .error import I21YError, TranslationNotFound
from .utils import locale_str