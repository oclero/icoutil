#!/usr/bin/env python3

import os
import unittest

from icoutil import IcoFile  # nopep8

TEST_RESOURCES_DIR = os.path.join(
  os.path.dirname(__file__), 'resources')


# Enable verbose mode for the lib.
IcoFile.verbose = True
IcoFile.verbose_level = 1


class TestIcoUtil(unittest.TestCase):
  def test_add_valid_image(self):
    ico = IcoFile()
    image_path = os.path.join(
      TEST_RESOURCES_DIR, 'directory/directory_16x16.png')
    success = True
    try:
      ico.add_png(image_path)
    except:
      success = False

    # Adding a valid image should work.
    self.assertEqual(success, True, "Adding an image with a valid size")

  def test_add_invalid_image(self):
    ico = IcoFile
    image_path = os.path.join(
      TEST_RESOURCES_DIR, 'directory/directory_17x17.png')
    success = True
    try:
      ico.add_png(image_path)
    except:
      success = False

    # It shouldn't be possible to have an incorrect size.
    self.assertEqual(success, False, "Adding an image with an invalid size")

  def test_add_already_existing_image(self):
    # Add a first time a 16x16 image.
    ico = IcoFile()
    ico.add_png(os.path.join(TEST_RESOURCES_DIR,
                'directory/directory_16x16.png'))
    success = True
    try:
      # Add a second time a 16x16 same image.
      ico.add_png(os.path.join(TEST_RESOURCES_DIR,
                  'document/document_16x16.png'))
    except:
      ico.close()
      success = False

    # It shouldn't be possible to have two images with the same size.
    self.assertEqual(
      success, False, "Adding an image for an already existing size")

  def test_add_individual_images(self):
    # Get binary data for an icon made from all images in a dir.
    ico = IcoFile()
    test_dir = os.path.join(TEST_RESOURCES_DIR, 'document')
    ico.add_png_dir(test_dir)
    data_1 = ico.get_ico_file_data()

    # Get binary data for an already existing icon.
    test_icon = os.path.join(TEST_RESOURCES_DIR, 'document/document.ico')
    with open(test_icon, 'rb') as file:
      data_2 = file.read()

    # The binary data should be the same.
    self.assertEqual(data_1, data_2, "Creating a .ICO from PNG files")


if __name__ == '__main__':
  os.chdir(os.path.dirname(__file__))
  unittest.main()
  exit()
