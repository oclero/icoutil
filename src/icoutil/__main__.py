#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import sys
from icoutil import IcoFile, __version__

if __name__ == '__main__':
   # Parse command-line arguments.
  parser = ArgumentParser(description=__doc__)
  parser.set_defaults(func=lambda _: parser.print_help(sys.stdout))
  parser.add_argument(
      '-v', '--version', action='version', version='icoutil ' + __version__)

  parser.add_argument('files', nargs='+', type=str,
                      help='Input .PNG filenames or directory')
  parser.add_argument('-o', '--output', default='icon.ico',
                      type=str, required=False, help='Output .ICO filename')
  args = parser.parse_args()

  # Create utility.
  ico = IcoFile.IcoFile()

  # Check if we have a directory path, or multiple PNG paths.
  if len(args.files) == 1 and os.path.isdir(args.files[0]):
    ico.add_png_dir(args.files[0])
  else:
    for file in args.files:
      ico.add_png(file)

  # Write file.
  ico.write(args.output)
