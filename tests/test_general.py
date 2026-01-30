from unittest.mock import MagicMock

import pytest

from i21y import TranslationNotFound, Translator
from i21y.loaders.file_ import Loader as FileLoaderBase
from i21y.loaders.json import Loader


def do_test_translator(t: Translator[Loader]) -> None:
    assert t("general.main") == "main"
    assert t("general.main", locale="ja") == "メイン"

    from i21y.utils import locale_str

    BASE = locale_str("wow.a")
    assert t(BASE.b) == "Layor B"
    assert t(BASE.b, locale="ja") == "B階層"

    assert t(BASE.c.d, "test_arg") == "Layor D: test_arg"
    assert t(BASE.c.d, "test_arg", locale="ja") == "D階層：test_arg"

    assert t(BASE.c.d, do_format=False) == r"Layor D: {}"


def test_translator() -> None:
    do_test_translator(Translator(Loader("tests/locale", False, False)))
    do_test_translator(Translator(Loader("tests/locale", do_not_search_file=True)))
    do_test_translator(Translator(Loader("tests/locale")))


def test_translation_not_found() -> None:
    """Test that TranslationNotFound is raised for non-existent keys."""
    t = Translator(Loader("tests/locale"))

    # Simple non-existent key
    with pytest.raises(TranslationNotFound):
        t("non_existent_key")

    # Nested non-existent key
    with pytest.raises(TranslationNotFound):
        t("general.non_existent")


def test_leaf_node_traversal() -> None:
    """Test accessing a child key of a string value (leaf node)."""
    t = Translator(Loader("tests/locale"))

    # "general.main" is "main" (string).
    # Accessing "general.main.sub" should fail.
    with pytest.raises(TranslationNotFound):
        t("general.main.sub")


def test_loader_cache_flags() -> None:
    """Test various Loader cache configurations."""

    # Case 1: No preload, no realtime cache, no file search -> Should find nothing
    loader_strict = Loader(
        "tests/locale",
        preload_cache=False,
        use_cache_realtime=False,
        do_not_search_file=True,
    )
    t_strict = Translator(loader_strict)

    with pytest.raises(TranslationNotFound):
        t_strict("general.main")

    # Case 2: Preload enabled, no file search allowed afterwards.
    # Since "general.main" exists, it should be in cache after init.
    loader_preload = Loader("tests/locale", preload_cache=True, do_not_search_file=True)
    t_preload = Translator(loader_preload)
    assert t_preload("general.main") == "main"


def test_no_realtime_cache() -> None:
    """Test that use_cache_realtime=False causes file to be re-loaded."""
    loader = Loader("tests/locale", preload_cache=False, use_cache_realtime=False)

    # Mock the load method to count calls
    original_load = loader.load
    loader.load = MagicMock(side_effect=original_load)  # type: ignore

    t = Translator(loader)

    # First call
    assert t("general.main") == "main"
    assert loader.load.call_count == 1

    # Second call - should load again because caching is disabled
    assert t("general.main") == "main"
    assert loader.load.call_count == 2


def test_realtime_cache_enabled() -> None:
    """Test that use_cache_realtime=True (default) caches the file."""
    loader = Loader("tests/locale", preload_cache=False, use_cache_realtime=True)

    original_load = loader.load
    loader.load = MagicMock(side_effect=original_load)  # type: ignore

    t = Translator(loader)

    # First call - loads file
    assert t("general.main") == "main"
    assert loader.load.call_count == 1

    # Second call - uses cache, load should NOT be called again
    assert t("general.main") == "main"
    assert loader.load.call_count == 1


def test_loader_search_default() -> None:
    """Test the 'default' argument in Loader.search."""
    loader = Loader("tests/locale")

    # Direct usage of loader.search with default value
    assert (
        loader.search("en", "non_existent", default="default_value") == "default_value"
    )

    # Confirm regular search works
    assert loader.search("en", "general.main") == "main"


def test_str_representations() -> None:
    """Test __str__ methods for debugging coverage."""
    loader = Loader("tests/locale")
    t = Translator(loader)

    assert str(t).startswith("<Translator loader=")

    # We need to access a LocaleFile to test its __str__
    # Search implementation details to get a LocaleFile instance
    f = loader.search_locale_file("en", "general.main")
    assert f is not None
    _, locale_file = f
    assert str(locale_file).startswith("<LocaleFile path=")

    # Test Caches __str__
    assert str(loader.caches).startswith("<Caches text=")


def test_loader_extensions_check() -> None:
    """Test that NotImplementedError is raised if EXTENSIONS is not set."""

    class BadLoader(FileLoaderBase):
        # EXTENSIONS is empty by default
        pass

    with pytest.raises(NotImplementedError):
        BadLoader("tests/locale")
