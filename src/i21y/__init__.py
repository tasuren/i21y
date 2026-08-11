__author__ = "Takagi Tasuku"
__version__ = "0.4.2"
__all__ = ("I21YError", "TranslationNotFound", "Translator", "locale_str")

from .error import I21YError, TranslationNotFound
from .translator import Translator
from .utils import locale_str
