from i21y import locale_str


BASE = locale_str("aiueo")
assert str(BASE) == "aiueo" and BASE.key == "aiueo"

KAGYO = locale_str("kakikukeko")
RIGHT = BASE / KAGYO
LEFT = BASE / str(KAGYO)
assert LEFT == RIGHT
assert str(LEFT) == str(RIGHT)
assert LEFT.test == RIGHT.test

assert BASE // "kakikukeko" == "aiueo.kakikukeko"