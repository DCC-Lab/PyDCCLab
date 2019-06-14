from dcclab.imageCollection import ZStack, ImageCollection
import numpy as np
import unittest

# Fixme: only tested Zstacks with 3D Arrays : test zStack/ImageCollection from image files


class TestZStackFrom3DArray(unittest.TestCase):

    def setUp(self):
        self.depth = 5
        self.grayStack = np.zeros((10, 10, self.depth))
        self.zStack = ZStack(self.grayStack)

    def testImageCollectionFrom3DArray(self):  # fixme: sorry for touching another class
        collection = ImageCollection(self.grayStack)

        self.assertTrue(len(collection) == self.depth)
        self.assertTrue(collection[0].shape == (10, 10))

    def testZStackFrom3DArray(self):
        self.assertTrue(len(self.zStack) == self.depth)
        self.assertTrue(self.zStack[0].shape == (10, 10))

    def testZStackShape(self):
        self.assertTrue(self.zStack.shape == (10, 10, 5))

    def testZStackLength(self):
        self.assertTrue(len(self.zStack) == 5)

    def testZStackGetArray(self):
        stackArray = self.zStack.getArray()
        self.assertIsInstance(stackArray, np.ndarray)
        self.assertTrue(stackArray.shape == (10, 10, 5))


class TestZStackFrom4DArray(unittest.TestCase):

    @unittest.skip("Collection from 4D arrays is Not Implemented")
    def testZStackFromRGBArray(self):
        RGBStack = np.zeros((40, 40, 10, 3))


class TestZStackFromImages(unittest.TestCase):

    def testImagesAreSimilar(self):
        pass

    def testZStackFromImages(self):
        pass

    # test all attributes
