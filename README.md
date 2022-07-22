<h1 align="center">
  <br>
  <img src="logo.png" alt="Gigapixel" height="260">
  <br>
  Gigapixel
  <br>
</h1>

<h4 align="center">Topaz Gigapixel AI automation tool</h4>

<p align="center">
    <img src="https://img.shields.io/pypi/v/gigapixel?color=orange" alt="PyPI">
    <img src="https://img.shields.io/pypi/pyversions/gigapixel?color=blueviolet" alt="Python 3">
    <img src="https://github.com/TimNekk/gigapixel/actions/workflows/tests.yml/badge.svg" alt="Tests">
</p>

<p align="center">
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## Requirements

[Topaz Gigapixel AI](https://www.topazlabs.com/gigapixel-ai) **v6** of **newer** required

## Installation

Install the current version with [PyPI](https://pypi.org/project/gigapixel/)

```bash
pip install -U gigapixel
```

## Usage

1. Create `Gigapixel` instance
2. Use `.process()` method to enhance image

```python
from gigapixel import Gigapixel, Scale, Mode
from pathlib import Path

# Path to Gigapixel executable file.
exe_path = Path('C:\Program Files\Topaz Labs LLC\Topaz Gigapixel AI\Topaz Gigapixel AI.exe')

# Output file suffix. (e.g. pic.jpg -> pic-gigapixel.jpg)
# You should set same value inside Gigapixel (File -> Preferences -> Default filename suffix).
output_suffix = '-gigapixel'

# Create Gigapixel instance.
app = Gigapixel(exe_path, output_suffix)

# Process image.
image = Path('path/to/image.jpg')
output_path = app.process(image, scale=Scale.X2, mode=Mode.STANDARD)

# Print output path.
print(output_path)
```

## Contributing

Bug reports and/or pull requests are welcome


## License

The module is available as open source under the terms of the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)
