<h1 align="center">
  <br>
  <img src="logo.png" alt="Gigapixel" height="260">
  <br>
  Gigapixel
  <br>
</h1>

<h4 align="center">Topaz Gigapixel AI automation tool</h4>

<p align="center">
    <img src="https://img.shields.io/pypi/v/gigapixel?style=for-the-badge" alt="PyPI">
    <img src="https://img.shields.io/pypi/pyversions/gigapixel?style=for-the-badge" alt="Python 3">
    <img src="https://img.shields.io/github/actions/workflow/status/TimNekk/Gigapixel/tests.yml?branch=main&label=TESTS&style=for-the-badge" alt="Tests">
</p>

<p align="center">
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## Requirements

Tested on [Topaz Gigapixel AI](https://www.topazlabs.com/gigapixel-ai) **v7.2.3**

## Installation

Install the latest version with [PyPI](https://pypi.org/project/gigapixel/)

```bash
pip install -U gigapixel
```

## Usage

```python
from gigapixel import Gigapixel

gp = Gigapixel(r"C:\Program Files\Topaz Labs LLC\Topaz Gigapixel AI\Topaz Gigapixel AI.exe")

gp.process(r"path\to\image.jpg")
```

Additional parameters can be passed to `process()` method:
```python
from gigapixel import Scale, Mode

gp.process(
  r"path\to\image.jpg",
  scale=Scale.X2,
  mode=Mode.STANDARD,
)
```

> **Warning!**
> Using parameters (`scale`, `mode`) may take **additional time** to process single image.
> Consider using them only when needed.
> To get the best performance, use `gp.process(r"path\to\image.jpg")`


## Contributing

Bug reports and/or pull requests are welcome


## License

The module is available as open source under the terms of the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)
