<div align="center">
<a href="https://github.com/oclero/icoutil">
	<img style="margin-bottom: 2em; width: 640px" src="https://raw.githubusercontent.com/oclero/icoutil/master/thumbnail.png">
</a>
</div>

# IcoUtil

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://mit-license.org/)
[![PyPi version](https://badgen.net/pypi/v/icoutil/)](https://pypi.org/project/icoutil)

A simple Python library to create `.ico` files (Windows icon file format) from `.png` files.

**Table of contents**

- [Install](#install)
- [Usage](#usage)
  - [As a library](#as-a-library)
  - [As a CLI program](#as-a-cli-program)
- [Remarks](#remarks)
- [Creator](#creator)
- [License](#license)

## Install

Use the [PyPi.org](https://pypi.org/project/icoutil) package index:

```sh
pip3 install icoutil
```

## Usage

### As a library

Two ways to use the library:

- Creating a `.ico` file from a single directory that contains multiple `.png` files:

  ```py
  import icoutil

  ico = icoutil.IcoFile()
  ico.add_png_dir('path/to/dir')
  ico.write('output.ico')
  ```

- Creating a `.ico` file from multiple `.png` files:

  ```py
  import icoutil

  ico = icoutil.IcoFile()
  ico.add_png('path/to/image1.png')
  ico.add_png('path/to/image2.png')
  ico.add_png('path/to/image3.png')
  ico.add_png('...')
  ico.write('output.ico')
  ```

### As a CLI program

Two ways to use the CLI:

- Creating a `.ico` file from a single directory that contains multiple `.png` files:

  ```sh
  icoutil --output "icon.ico" "path/to/dir"
  ```

- Creating a `.ico` file from multiple `.png` files:

  ```sh
  icoutil --output "icon.ico" "path/to/image1.png" "path/to/image2.png" "path/to/image3.png" ...
  ```

## Remarks

- The file specification can be read [here](<https://en.wikipedia.org/wiki/ICO_(file_format)>).
- The following sizes are used by Windows, but not all required:
  - 16×16
  - 20×20
  - 24×24
  - 32×32
  - 40×40
  - 48×48
  - 64×64
  - 96×96
  - 128×128
  - 256×256
- This library won't consider sizes outside the ones specified above.
- The maximum allowed size is 256×256 pixels.

## Creator

**Olivier Cléro** | [email](mailto:oclero@pm.me) | [website](https://www.olivierclero.com) | [github](https://www.github.com/oclero) | [gitlab](https://www.gitlab.com/oclero)

## License

This project is available under the MIT license. See the [LICENSE](LICENSE) file for more info.
