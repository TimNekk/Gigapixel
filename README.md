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

[Topaz Gigapixel AI](https://www.topazlabs.com/gigapixel-ai) **v6.1.0** or **newer** required

## Installation

Install the current version with [PyPI](https://pypi.org/project/gigapixel/)

```bash
pip install -U gigapixel
```

## Usage

1. Create `Gigapixel` instance
2. Use `.process()` method to enhance image

```python
from gigapixel import Gigapixel, Scale, Mode, OutputFormat
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
output_path = app.process(image)

# Print output path.
print(output_path)
```

Additional parameters can be passed to `process()` method **(Takes additional time)**:
```python
from gigapixel import Scale, Mode, OutputFormat

output_path = app.process(image, scale=Scale.X2, mode=Mode.STANDARD, delete_from_history=True, output_format=OutputFormat.PNG)
```

> **Warning!**
> Using parameters (`scale`, `mode`, `output_format`, `delete_from_history`) will take **additional time** to process single image.
> Consider using them only when needed.
> To get the best performance, use `app.process(image)`


## Contributing

Bug reports and/or pull requests are welcome


## License

The module is available as open source under the terms of the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0)
