[![PyPI](https://img.shields.io/pypi/v/i21y)](https://pypi.org/project/i21y/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/i21y)
![PyPI - Downloads](https://img.shields.io/pypi/dm/i21y)
![PyPI - License](https://img.shields.io/pypi/l/i21y)
[![Documentation Status](https://readthedocs.org/projects/i21y/badge/?version=latest)](https://i21y.readthedocs.io/en/latest/?badge=latest)
[![Buy Me a Coffee](https://img.shields.io/badge/-tasuren-E9EEF3?label=Buy%20Me%20a%20Coffee&logo=buymeacoffee)](https://www.buymeacoffee.com/tasuren)

# i21y
i21y (a.k.a internationalization.py) is library for support i18n in Python. It is easy to use.

**Features:**
- Zero dependencies by default
- Simple design
- Utilities to simplify keys

## Installation
Normal: `pip install i21y`  
YAML support: `pip install i21y[yaml]`  
Fast JSON (by orjson) support: `pip install i21y[fast-json]`

## Example
### Basic
```python
from i21y import Translator
from i21y.loaders.json import Loader

t = Translator(Loader("locale"))

assert t("main.responses.not_found", locale="ja") == "見つからなかった。"
```
### Advanced
```python
from i21y import locale_str

LONG_KEY = locale_str("very.long.locale.key.yeah_so_long")
print(LONG_KEY.but_easy_to_use) # very.long.locale.key.yeah_so_long.but_easy_to_use

assert t(LONG_KEY.but_easy_to_use, locale="ja") == "とても長いキーでも簡単に使える。"
assert t(LONG_KEY + "but_easy_to_use", locale="ja") == "とても長いキーでも簡単に使える。"
```

## Documentation
See the [documentation](https://i21y.readthedocs.io/) for usage and details.

## Contributing Guide
This project is managed by the package manager PDM.  
In coding, please use Black as a code formatter and pyright for type checking. The configuration is described in `pyproject.toml`.  
Please write what you have done in a complete sentence and use the original form of the verb. e.g. `Fix that locale_str can't join`.
