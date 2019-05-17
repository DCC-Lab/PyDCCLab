import czi_util
import unittest
import czifile
import numpy as np
from unittest.mock import Mock, patch
import matplotlib.pyplot


class TestCziUtil(unittest.TestCase):

    def test_read_czi_file(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        self.assertIsInstance(czi, czifile.CziFile)
        czi_util.close(czi)

    def test_read_czi_file_invalid(self):
        with self.assertRaises(FileNotFoundError):
            czi_util.read_czi_file("test_czi_.czi")

    def test_read_czi_file_invalid_not_czi(self):
        with self.assertRaises(ValueError):
            czi_util.read_czi_file("test_pas_czi.jpg")

    def test_close(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        czi_util.close(czi)
        with self.assertRaises(RuntimeError):
            czi_util.get_images_from_czi_image(czi)

    def test_extract_metadata_no_save(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        metadata = czi_util.extract_metadata(czi)
        self.assertIsInstance(metadata, str)
        czi_util.close(czi)

    def test_extract_metadata_save(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        czi_util.extract_metadata(czi, "test_meta")
        czi_util.close(czi)
        ok = True
        try:
            file = open("test_meta.xml", "r")
            file.close()
        except FileNotFoundError:
            ok = False

        self.assertTrue(ok)

    def test_extract_array(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        array = czi_util.get_array_from_czi_image(czi)
        czi_util.close(czi)
        self.assertIsInstance(array, np.ndarray)

    def test_extract_array_shape(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        array = czi_util.get_array_from_czi_image(czi)
        czi_util.close(czi)
        self.assertEqual(array.shape, (1, 2, 1460, 1936, 1))

    def test_extract_images(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        images = czi_util.get_images_from_czi_image(czi)
        czi_util.close(czi)
        self.assertIsInstance(images, np.ndarray)

    def test_extract_images_nb_images(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        images = czi_util.get_images_from_czi_image(czi)
        nb_images = images.shape[0]
        czi_util.close(czi)
        self.assertEqual(nb_images, 2)

    @patch("matplotlib.pyplot.show", new=Mock)
    def test_show_images(self):
        czi = czi_util.read_czi_file("test_czi.czi")
        images = czi_util.show_images_from_czi_image(czi)
        czi_util.close(czi)
        self.assertIsInstance(images, np.ndarray)
