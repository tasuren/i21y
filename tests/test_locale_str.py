from i21y import locale_str


def test_locale_str() -> None:
    BASE = locale_str("aiueo")
    assert str(BASE) == "aiueo" and BASE.key == "aiueo"

    KAGYO = locale_str("kakikukeko")
    RIGHT = BASE + KAGYO
    LEFT = BASE + str(KAGYO)
    assert LEFT == RIGHT
    assert str(LEFT) == str(RIGHT)
    assert LEFT.test == RIGHT.test

    assert BASE & "kakikukeko" == "aiueo.kakikukeko"

    assert BASE.join("test", a="b").extras["a"] == "b"
    assert BASE.test.update_extras(a="b").extras["a"] == "b"


def test_locale_str_equality_and_ops() -> None:
    """Additional coverage for locale_str operations."""
    ls = locale_str("key")

    # Test __ne__
    assert ls != locale_str("other")
    assert ls != "key"  # Not a locale_str instance

    # Test __eq__
    assert ls == locale_str("key")

    # Test __add__ with iterable
    ls_iter = locale_str("start") + ["mid", "end"]
    assert ls_iter.key == "start.mid.end"
