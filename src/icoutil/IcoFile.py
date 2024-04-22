#!/usr/bin/env python3

import os
from typing import Tuple
import weakref
from PIL import Image

# Convenient alias for (width, height).
Size = Tuple[int, int]

# The .ICO specification does allow any size from 1x1 to 256x256, but Windows
# needs these sizes.
STANDARD_ICO_SIZES: list[Size] = [(16, 16),
                                  (20, 20),
                                  (24, 24),
                                  (32, 32),
                                  (40, 40),
                                  (48, 48),
                                  (64, 64),
                                  (96, 96),
                                  (128, 128),
                                  (256, 256)]


class IcoFile:
  '''
  Represents an .ICO file.

  Attributes:
      verbose (bool): enable/disable verbose output to console.
  '''

  # Enable/disable verbose output to console (class-wide).
  verbose: bool = False

  # Enable/disable verbose output to console (class-wide).
  verbose_level: int = 0

  def __init__(self):
    '''
    Constructor.
    '''

    # Stores a mapping size -> Image.
    self.size_map: dict[Size, Image.Image] = {}
    self._finalizer = weakref.finalize(
      self, self._close_files, list(self.size_map.values()))

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):  # type: ignore
    self.close()

  def __del__(self):
    self.close()

  def __str__(self) -> str:
    '''
    Prints the data structure.
    '''
    output = '{\n'
    for size, image in self.size_map.items():
      output += f'  {size}: "{image.filename}"\n'  # type: ignore
    output += '}'

    return output

  def add_png_dir(self, path: str) -> None:
    '''
    Adds all the PNG files in the directory.
    '''
    # Check directory existence.
    if not os.path.isdir(path):
      raise Exception(f'The following path is not a directory: {path}')

    # Get all .PNG files in the directory.
    png_files = [os.path.join(path, f) for f in os.listdir(
      path) if f.lower().endswith('.png')]

    # Warn the user if no PNG found.
    if len(png_files) == 0:
      print(
        f'Warning! The following directory does not contain any PNG file: {path}')

    # Add all PNG images in that directory.
    for png_file in png_files:
      self.add_png(png_file)

  def add_png(self, path: str) -> None:
    '''
    Adds a PNG file.
    '''
    # Check if the file exists.
    if not os.path.exists(path):
      raise Exception(f'This file does not exist: "{path}"')

    # Check if the file is a PNG image.
    _, extension = os.path.splitext(path)
    if not os.path.isfile(path) or extension.lower() != '.png':
      raise Exception(f'This path is not a .PNG file: "{path}"')

    # Check if the PNG image's size is valid.
    image = Image.open(path)
    if not image.size in STANDARD_ICO_SIZES:
      image.close()
      raise Exception(
        f'This PNG image has an invalid size ({image.size[0]}, {image.size[1]}): {path}')

    # Check if the size isn't already taken by another image.
    if image.size in self.size_map:
      other_image = self.size_map[image.size]
      image.close()
      raise Exception(
        f'The size {image.size} is already taken this image: {other_image.filename}')

    # Add the image to the list.
    self.size_map[image.size] = image

    # Keep the dict sorted. Not mandatory, but it's considered a good practice
    # to have the icons sorted in the .ICO file.
    self.size_map = dict(sorted(self.size_map.items()))

    # (Verbose): Print.
    if IcoFile.verbose:
      print(f'Added {str(image.size):<10}: "{path}"')

  def remove_size(self, size: Size) -> None:
    '''
    Removes the PNG file that has the size in parameter.
    '''
    if size in self.size_map:
      del self.size_map[size]
      print(f'Removed size: {size}')
    elif IcoFile.verbose:
      print(f'Size {size} not present: cannot remove')

  def remove_png(self, path: str) -> None:
    '''
    Removes the .PNG file.
    '''
    for size, value in self.size_map.items():
      if value.filename == path:  # type: ignore
        value.close()
        del self.size_map[size]
        print(f'Removed: "{path}"')
        return

    if IcoFile.verbose:
      print(f'File not present: {path}')

  def write(self, path: str) -> None:
    '''
    Writes the icon to a .ICO file
    '''
    # Check if the file is an ICO image.
    _, extension = os.path.splitext(path)
    if len(extension) == 0:
      raise Exception('Output file has no extension. It should be .ICO.')
    elif extension.lower() != '.ico':
      print(
        f"Warning! Output file has a {extension.capitalize()} extension instead of .ICO.")

    # Check if at least one file is present.
    if len(self.size_map) == 0:
      raise Exception(
        f"At least one PNG must be present. The icon can't be empty.")

    # Get binary data.
    data = self.get_ico_file_data()

    # Write image to disk.
    output_dir = os.path.dirname(path)
    os.makedirs(output_dir, exist_ok=True)
    with open(path, 'wb') as f:
      f.write(data)
    if IcoFile.verbose:
      print(f'Written: "{path}"')

    # (Verbose) Print missing sizes.
    if IcoFile.verbose:
      missing_sizes = self.get_missing_sizes()
      if len(missing_sizes) > 0:
        missing_sizes_str = ', '.join(f'({w}, {h})' for w, h in missing_sizes)
        print(f'[Info] Some sizes we missing: {missing_sizes_str}')

  def get_missing_sizes(self) -> list[Size]:
    '''
    Gets the missing sizes.
    Note: it's not mandatory to have all sizes.
    '''
    return list(set(STANDARD_ICO_SIZES) - set(list(self.size_map.keys())))

  def get_ico_file_data(self) -> bytes:
    '''
    Creates data according to the .ICO file specification.
    Source: https://en.wikipedia.org/wiki/ICO_(file_format)
    '''
    BYTE_ORDER = 'little'
    image_count = len(self.size_map)

    # Header.
    HEADER_SIZE = 6
    data = bytes([0, 0])  # Reserved. Must always be 0.
    data += bytes([1, 0])  # Image type: 1 for icon (.ICO) image.
    data += bytes([image_count, 0])  # Number of images in the file.
    offset = HEADER_SIZE

    # Structure of image directory: one entry per image.
    ENTRY_BYTE_SIZE = 16
    offset += image_count * ENTRY_BYTE_SIZE  # Anticipate total entries size.
    for size, image in self.size_map.items():
      # Value 0 means image width is 256 pixels.
      w = 0 if size[0] == 256 else size[0]
      h = 0 if size[1] == 256 else size[1]

      data += bytes([w, h])  # Image width and height in pixels.
      data += bytes([0])  # Nb of colors in the color palette. 0 if no palette.
      data += bytes([0])  # Reserved. Should be 0.
      data += bytes([1, 0])  # Nb of color planes.
      data += bytes([32, 0])  # Bits per pixel.

      byte_size = os.path.getsize(image.filename)  # type: ignore
      # size of image data.
      data += byte_size.to_bytes(4, byteorder=BYTE_ORDER)
      data += offset.to_bytes(4, byteorder=BYTE_ORDER)  # Points to image date.
      offset += byte_size  # Next image data offset.

    # Data for all images.
    for _, image in self.size_map.items():
      with open(image.filename, 'rb') as f:  # type: ignore
        data += f.read()

    return data

  def get_png_for_size(self, size: Size) -> str | None:
    '''
    Gets the image associated to the size in parameter,
    or None if no image is associtated to this size.
    '''
    if size in self.size_map:
      return self.size_map[size].filename  # type: ignore
    else:
      return None

  def close(self):
    '''
    Closes the file handles.
    '''
    IcoFile._close_files(list(self.size_map.values()))

  @staticmethod
  def _close_files(images: list[Image.Image]):
    for image in images:
      if IcoFile.verbose and IcoFile.verbose_level > 0:
        print(f'Closing file    : "{image.filename}"')  # type: ignore
      image.close()
