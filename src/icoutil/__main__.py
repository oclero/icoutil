#!/usr/bin/env python3

from argparse import ArgumentParser
import os
from icoutil import IcoFile, __version__


def make_argparser():
  # Parse command-line arguments.
  parser = ArgumentParser(description=__doc__)
  parser.add_argument(
      '-v', '--version', action='version', version=f'icoutil v{__version__}')

  parser.add_argument('files', nargs='+', type=str,
                      help='Input .PNG filenames or directory')
  parser.add_argument('-o', '--output', default='icon.ico',
                      type=str, required=False, help='Output .ICO filename')
  parser.add_argument('-V', '--verbose', action='store_true',
                      help='Enable verbose mode')
  args = parser.parse_args()
  return args


def create_ico(files: list[str], output_path: str, verbose: bool) -> None:
  # Create utility.
  IcoFile.verbose = verbose
  ico = IcoFile()

  # Check if we have a directory path, or multiple PNG paths.
  if len(files) == 1 and os.path.isdir(files[0]):
    ico.add_png_dir(os.path.abspath(files[0]))
  else:
    for file in files:
      ico.add_png(os.path.abspath(file))

  # Write file.
  ico.write(output_path)


if __name__ == '__main__':
  args = make_argparser()
  create_ico(args.files[1:], os.path.abspath(args.output), args.verbose)
