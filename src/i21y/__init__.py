__author__ = "Takagi Tasuku"
__version__ = "0.2.0"
__all__ = ("Translator", "I21YError", "TranslationNotFound", "locale_str")

from .translator import Translator
from .error import I21YError, TranslationNotFound
from .utils import locale_str
