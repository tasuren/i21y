[![PyPI](https://img.shields.io/pypi/v/i21y)](https://pypi.org/project/i21y/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/i21y) ![PyPI - Downloads](https://img.shields.io/pypi/dm/i21y) ![PyPI - License](https://img.shields.io/pypi/l/i21y) [![Documentation Status](https://readthedocs.org/projects/i21y/badge/?version=latest)](https://i21y.readthedocs.io/en/latest/?badge=latest) [![Buy Me a Coffee](https://img.shields.io/badge/-tasuren-E9EEF3?label=Buy%20Me%20a%20Coffee&logo=buymeacoffee)](https://www.buymeacoffee.com/tasuren)
# i21y
i21y (a.k.a internationalization.py) is library for support i18n in Python. It is easy to use.

## Example
```python
from i21y import Translator
from i21y.loaders.json import Loader

t = Translator(Loader("locale"))
```