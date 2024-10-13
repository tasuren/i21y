from i21y import Translator
from i21y.loaders.yaml import Loader


def do_test_translator(t: Translator[Loader]) -> None:
    assert t("main.test") == "Test"
    assert t("main.test", locale="ja") == "テスト"

    assert t("main.a.b.c") == "See"
    assert t("main.a.b.c", locale="ja") == "しー"

    assert t("main.a.b.d.e") == "Yee"
    assert t("main.a.b.d.e", locale="ja") == "いー"

    assert t("main.a.b.f") == "Eff:ect"
    assert t("main.a.b.f", locale="ja") == "エフ：ェクト"


do_test_translator(Translator(Loader("tests/locale")))
