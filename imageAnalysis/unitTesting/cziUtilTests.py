from imageAnalysis import cziUtil
import unittest
import czifile
import numpy as np
from unittest.mock import Mock, patch



class TestCziUtil(unittest.TestCase):

    def TestReadCziFile(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        self.assertIsInstance(czi, czifile.CziFile)
        cziUtil.closeCziFileObject(czi)

    def testReadCziFileInvalid(self):
        with self.assertRaises(FileNotFoundError):
            cziUtil.readCziImage("test_czi_.czi")

    def testReadFileNotCzi(self):
        with self.assertRaises(ValueError):
            cziUtil.readCziImage("testNotCziFile.jpg")

    def testClose(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        cziUtil.closeCziFileObject(czi)
        with self.assertRaises(RuntimeError):
            cziUtil.getImagesFromCziFileObject(czi)

    def testExtractMetadatNoSave(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        metadata = cziUtil.extractMetadataFromCziFileObject(czi)
        self.assertIsInstance(metadata, str)
        cziUtil.closeCziFileObject(czi)

    def testExtractMetadataSave(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        cziUtil.extractMetadataFromCziFileObject(czi, "test_meta")
        cziUtil.closeCziFileObject(czi)
        ok = True
        try:
            file = open("test_meta.xml", "r")
            file.close()
        except FileNotFoundError:
            ok = False

        self.assertTrue(ok)

    def testExtractArray(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        array = cziUtil.getArrayFromCziFileObject(czi)
        cziUtil.closeCziFileObject(czi)
        self.assertIsInstance(array, np.ndarray)

    def testExtractArrayShape(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        array = cziUtil.getArrayFromCziFileObject(czi)
        cziUtil.closeCziFileObject(czi)
        self.assertEqual(array.shape, (1, 2, 1460, 1936, 1))

    def testExtractImages(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        images = cziUtil.getImagesFromCziFileObject(czi)
        cziUtil.closeCziFileObject(czi)
        self.assertIsInstance(images, np.ndarray)

    def testExtractNumberImages(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        images = cziUtil.getImagesFromCziFileObject(czi)
        nb_images = images.shape[0]
        cziUtil.closeCziFileObject(czi)
        self.assertEqual(nb_images, 2)

    @patch("matplotlib.pyplot.show", new=Mock)
    def testShowImages(self):
        czi = cziUtil.readCziImage("testCziFile.czi")
        images = cziUtil.showImagesFromCziFileObject(czi)
        cziUtil.closeCziFileObject(czi)
        self.assertIsInstance(images, np.ndarray)
