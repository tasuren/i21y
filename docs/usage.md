# Usage
## Loader
It is used to load translations.
In this case, use `i21y.loaders.json.Loader` to load json and set the locale directory `locale`.
```python
from i21y.loaders.json import Loader

loader = Loader("locale")
```
Create `en` and `ja` directory to place English and Japanese text.

## Translator
Translator is the class to translate text.
```python
from i21y import Translator

t = Translator(loader)
```
Now, you can translate text by `Translator.translate`.
You must pass the key of path to text.
It specifies the slash in the path as a dot and the value in the file as if were an attribute.
And you can specify locale by keyword arguments `locale`.
For example, the following code, accesses to `responses.success` on `locale/{en,ja}/http/general.json`.
```python
assert t.translate("http.general.responses.success") == "Success!"
assert t.translate("http.general.responses.success", locale="ja") == "成功した！"
```
It also can be called as instance.  
```python
assert t("http.general.responses.success") == "Success!"
assert t("http.general.responses.success", locale="ja") == "成功した！"
```
If you want format the text, you can embed a value into text. It uses `str.format` to format.
The following code, text is `"{file_name} is not found."`.
```python
assert t(
    "http.general.responses.not_found",
    file_name="robots.txt"
) == "robots.txt is not found"
```

## locale_str
"Oh, the key is so long, I don't need to write it."
For over it, you can use `i21y.utils.locale_str` (`i21y.locale_str`).
It is useful for concatenating keys.
```python
from i21y import locale_str

LOCALE = locale_str("main.http.general.responses")

assert LOCALE.not_found == locale_str("http.general.responses.not_found")
assert LOCALE + "not_found" == locale_str("http.general.responses.not_found")
assert t(LOCALE.not_found, file_name="../secret.key") == "../secret.key is not found."

assert str(LOCALE.not_found) == "http.general.responses.not_found"
assert LOCALE & "not_found" == "http.general.responses.not_found"
```

## yaml support
You can use yaml by installing `pyyaml` or `i21y[yaml]`.
