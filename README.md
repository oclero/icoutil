# Icoutil

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://mit-license.org/)
[![PyPi version](https://badgen.net/pypi/v/pip/)](https://pypi.org/project/icoutil)

A simple Python library to create .ICO files (Windows icon file format).

**Table of contents**

- [Install](#install)
- [Usage](#usage)
  - [As a library](#as-a-library)
  - [As a CLI program](#as-a-cli-program)
- [Creator](#creator)
- [License](#license)

## Install

Use the PyPi.org index:

```sh
pip3 install icoutil
```

## Usage

### As a library

Two ways to use the library:

- Creating a `.ico` file from a single directory that contains multiple PNG files

  ```py
  import icoutil

  ico = icoutil.IcoFile()
  ico.add_png_dir('path/to/dir')
  ico.write('output.ico')
  ```

- Creating a `.ico` file from multiple PNG files:

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

- Creating a `.ico` file from a single directory that contains multiple PNG files

  ```sh
  icoutil --output "icon.io" "path/to/dir"
  ```

- Creating a `.ico` file from multiple PNG files:

  ```sh
  icoutil --output "icon.io" "path/to/image1.png" "path/to/image2.png" "path/to/image3.png" ...
  ```

## Creator

**Olivier Cléro** | [email](mailto:oclero@pm.me) | [website](https://www.olivierclero.com) | [github](https://www.github.com/oclero) | [gitlab](https://www.gitlab.com/oclero)

## License

This project is available under the MIT license. See the [LICENSE](LICENSE) file for more info.
