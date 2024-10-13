from i21y import Translator
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


do_test_translator(Translator(Loader("tests/locale", False, False)))
do_test_translator(Translator(Loader("tests/locale", do_not_search_file=True)))
do_test_translator(Translator(Loader("tests/locale")))
